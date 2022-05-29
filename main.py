# from connection import conn
from tornado.web import Application, RequestHandler
import json
import os
import asyncio
import psycopg
from psycopg.rows import dict_row

class MainHandler(RequestHandler):

    def get(self):

        self.render("test.html")
    
class Test_request(RequestHandler):

    def get(self):
        self.render("index.html")

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self):

        table = self.get_argument('name')

        async with await psycopg.AsyncConnection.connect(host='*',
                        port='*',
                        dbname='*',
                        user='*',
                        password='*',
                        target_session_attrs='*',
                        sslmode='*', autocommit=False) as aconn:
            async with aconn.cursor(row_factory=dict_row) as acur:
                res = await acur.execute(f"""SELECT * from {table};""")
                res = await acur.fetchall()
                res = json.dumps(res, indent=4, sort_keys=True, ensure_ascii=False, default=str)
                # await res
    
        # query = f"""SELECT * from {table};"""
        # conn.execute(query)
        # res = dict_cur.fetchall()
        # res = json.dumps(res, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        self.write(res)


def make_app():

    settings = dict(xsrf_cookies=True, autoreload=True, debug=True, autoescape=None,
    template_path=os.path.join(os.path.dirname(__file__), "templates"))
    app = Application([
        ('/index.html', Test_request),
        ("/test.html", MainHandler)],
        **settings)
    
    return app


async def main():

    app = make_app()
    port = 8888
    app.listen(port)
    print(f"Server Listening on Port {8888}")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
