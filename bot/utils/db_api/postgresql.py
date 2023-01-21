import asyncio
from typing import Union
import logging
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command: object, *args: object,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ) -> object:
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        lang varchar(2) DEFAULT('en'),
        user_id BIGINT NOT NULL UNIQUE,
        phone varchar(20) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, user_id) VALUES($1, $2, $3) returning *"
        logging.debug(f"request>>>\n{sql}")
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def update_phone(self, phone, user_id):
        sql = "UPDATE users SET phone=$1 WHERE user_id=$2"
        await self.execute(sql, phone, user_id, execute=True)

    async def get_user_id(self, user_id):
        sql = "SELECT user_id FROM basket WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def get_lang(self, user_id):
        return await self.execute(f"select lang from users where user_id = {user_id}", fetchval=True)

    async def update_lang(self, user_id, lang):
        sql = "UPDATE users SET lang=$1 WHERE user_id=$2"
        return await self.execute(sql, lang, user_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def select_phone(self, user_id):
        sql = "SELECT phone FROM users WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username=$1 WHERE user_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_name(self, user_id, new_name):
        sql = "UPDATE users SET full_name=$1 WHERE user_id=$2"
        await self.execute(sql, new_name, user_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    async def delete_basket_item(self, basket_id):
        sql = "DELETE FROM basket WHERE id=$1"
        return await self.execute(sql, basket_id, execute=True)

    """
    menu_lunch table contents
    """

    async def create_table_menu_lunch(self):
        sql = """
        CREATE TABLE IF NOT EXISTS menu_lunch (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price_full INTEGER NOT NULL,
        price_par INTEGER NOT NULL,
        full_text_uz VARCHAR(255) NOT NULL,
        full_text_en VARCHAR(255) NOT NULL,
        full_text_ru VARCHAR(255) NOT NULL,
        par_text_uz VARCHAR(255) NOT NULL,
        par_text_en VARCHAR(255) NOT NULL,
        par_text_ru VARCHAR(255) NOT NULL,
        photo VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_menu_dinner(self):
        sql = """
        CREATE TABLE IF NOT EXISTS menu_dinner (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price_full INTEGER NOT NULL,
        price_par INTEGER NOT NULL,
        full_text_uz VARCHAR(255) NOT NULL,
        full_text_en VARCHAR(255) NOT NULL,
        full_text_ru VARCHAR(255) NOT NULL,
        par_text_uz VARCHAR(255) NOT NULL,
        par_text_en VARCHAR(255) NOT NULL,
        par_text_ru VARCHAR(255) NOT NULL,
        photo VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def get_menu(self, menu_name):
        sql = "SELECT * FROM menu_lunch WHERE name = $1"
        return await self.execute(sql, menu_name, fetchrow=True)

    async def get_menu_with_id_lunch(self, menu_id, user_id):
        user_lang = await self.get_lang(user_id)
        sql = f"select id ,full_text_{user_lang} as text_full, par_text_{user_lang} as text_par ,price_full, price_par,  photo from menu_lunch where id = $1"
        return await self.execute(sql, menu_id, fetchrow=True)

    async def get_menu_with_id_dinner(self, menu_id, user_id):
        user_lang = await self.get_lang(user_id)
        sql = f"select id ,full_text_{user_lang} as text_full, par_text_{user_lang} as text_par ,price_full, price_par,  photo from menu_dinner where id = $1"
        return await self.execute(sql, menu_id, fetchrow=True)

    """ENOUGH FOR MENU"""

    """Table of basket"""

    async def create_table_basket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS basket (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        menu_id INTEGER NOT NULL,
        menu_type VARCHAR(10) DEFAULT('full'),
        address_lat real NULL,
        address_lon real NULL,
        comment VARCHAR(255) NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        event varchar(10) DEFAULT('lunch'),
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (menu_id) REFERENCES menu_lunch (id)
        );
        """
        await self.execute(sql, execute=True)

    async def add_basket(self, user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment, event):
        basket_id = await self.check_basket(user_id, menu_id, event, menu_type)
        if basket_id:
            await self.update_basket(basket_id, quantity)
            return
        sql = "INSERT INTO basket (user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment, event) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        return await self.execute(sql, user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment,
                                  event, execute=True)

    async def update_basket(self, id, quantity):
        sql = "UPDATE basket SET quantity= quantity + $1 WHERE id=$2 "
        return await self.execute(sql, quantity, id, execute=True)

    async def check_basket(self, user_id, menu_id, event, menu_type='full'):
        sql = "SELECT id FROM basket WHERE user_id = $1 AND menu_id = $2 AND event = $3 AND menu_type = $4"
        return await self.execute(sql, user_id, menu_id, event, menu_type, fetchval=True)

    async def get_basket_user(self, user_id):
        lang = await self.get_lang(user_id)
        sql = f"select basket.id, menu_lunch.name, full_text_{lang} as full_text, par_text_{lang} as par_text, basket.menu_type, basket.quantity, " \
              "basket.price, basket.event from basket inner join menu_lunch on basket.menu_id = menu_lunch.id where basket.user_id = $1"
        return await self.execute(sql, user_id, fetch=True)

    ##TODO: add dinner menu to basket last work herreeeee

    async def get_basket_order(self):
        sql = """SELECT users.full_name, users.phone, users.user_id, menu_lunch.name, 
        basket.menu_type, basket.quantity, basket.price, basket.address_lat, basket.address_lon, basket.comment FROM basket 
        INNER JOIN menu_lunch ON basket.menu_id = menu_lunch.id 
        INNER JOIN users ON basket.user_id = users.user_id"""

    async def increase_quantity(self, basket_id):
        sql = "UPDATE basket SET quantity=quantity+1 WHERE id=$1"
        return await self.execute(sql, basket_id, execute=True)

    async def decrease_quantity(self, basket_id):
        sql = "UPDATE basket SET quantity=quantity-1 WHERE id=$1"
        return await self.execute(sql, basket_id, execute=True)

    async def basket_is_empty(self, user_id):
        return await self.execute("select count(*) from basket where user_id=$1", user_id, fetchval=True)

    async def clear_basket(self,user_id: int):
        await self.execute("delete from basket where user_id = $1", user_id, execute=True)
    """Table of orders"""

    async def create_table_orders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL,
        menu_id INTEGER NOT NULL,
        menu_type VARCHAR(10) DEFAULT('full'),
        address_lat real NULL,
        address_lon real NULL,
        comment VARCHAR(255) NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        event varchar(10) DEFAULT('lunch'),
        order_time TIMESTAMP NULL,
        is_paid BOOLEAN DEFAULT(FALSE),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (menu_id) REFERENCES menu_lunch(id)
        );
        """
        await self.execute(sql, execute=True)

    async def add_order(self, user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment, event):
        sql = "INSERT INTO orders (user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment, event) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        return await self.execute(sql, user_id, menu_id, menu_type, address_lat, address_lon, quantity, price, comment,
                                  event,
                                  execute=True)

    async def insert_orders(self, user_id):
        order_id = await self.execute("select max(order_id) from orders", fetchval=True)
        sql = """Insert into orders(order_id,user_id, full_name, phone, menu_id, menu_type, address_lon, address_lat, comment, quantity, price, event, order_time, is_paid)
                       select $1 ,users.user_id, users.full_name, users.phone, menu_lunch.id, basket.menu_type, basket.address_lon, basket.address_lat,
                       basket.comment,  basket.quantity,basket.price , basket.event , now(), FALSE from basket
                       inner join menu_lunch on basket.menu_id = menu_lunch.id
                       inner join users on users.user_id=basket.user_id where basket.user_id = $2 ;"""
        print(order_id)
        if order_id:
            await self.execute(sql, order_id+1, user_id, execute=True)
            await asyncio.sleep(1)
            sql = f"select * from orders where user_id = $1  and order_id =$2;"
            return await self.execute(sql, user_id, order_id + 1, fetch=True)
        order_id = 1
        await self.execute(sql, order_id, user_id, execute=True)
        await asyncio.sleep(2)
        sql = f"select * from orders where user_id = $1  and order_id =$2;"
        return await self.execute(sql, user_id, order_id , fetch=True)


    async def get_order_user_full(self, user_id, order_id):
        sql = """select users.full_name,users.phone, menu_lunch.name as menu, orders.address_lon, orders.address_lat, orders.menu_type, orders.quantity,
                  orders.price ,orders.event, orders.order_time  from orders
                  inner join menu_lunch on orders.menu_id = menu_lunch.id
                  inner join users on users.user_id=orders.user_id where orders.user_id = $1 and orders.order_id = $2"""
        return await self.execute(sql, user_id, order_id, fetch=True)

    async def update_paid(self, order_id):
        sql = "UPDATE orders SET is_paid = TRUE, order_time = now() WHERE id = $2"
        return await self.execute(sql, order_id, execute=True)
