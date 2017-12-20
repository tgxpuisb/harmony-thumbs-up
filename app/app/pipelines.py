# -*- coding: utf-8 -*-
import pymysql
from .config import password, host, user, database


class AppPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(host, user, password, database)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        if spider.name == 'project':
            self.handle_project(item)
        elif spider.name == 'project_to_user':
            self.handle_project2user(item)
        elif spider.name == 'user_detail':
            self.handle_user_detail(item)
        return item

    def close_spider(self, spider):
        self.db.close()

    def handle_project(self, item):
        if item['name']:
            select_sql = "SELECT * FROM project WHERE `name` = '%s'" % (item['name'])
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall()
            if len(results) == 0:
                insert_sql = "INSERT INTO project \
                (`name`, stars, forks, commits, issues, create_time)\
                VALUES ('%s', %s, %s, %s, %s, %s)" \
                % (item['name'], item['stars'], item['forks'], item['commits'], item['issues'], item['create_time'])
                print(insert_sql)
                self.cursor.execute(insert_sql)
                self.db.commit()
            else:
                update_sql = "UPDATE project SET \
                stars=%s, forks=%s, commits=%s, issues=%s, create_time=%s WHERE \
                `name`='%s'" \
                % (item['stars'], item['forks'], item['commits'], item['issues'], item['create_time'], item['name'])

                print(update_sql)
                self.cursor.execute(update_sql)
                self.db.commit()

    def handle_project2user(self, item):
        if item['name']:
            select_sql = "SELECT * FROM user WHERE `name` = '%s'" % (item['name'])
            self.cursor.execute(select_sql)
            results = self.cursor.fetchall()
            if len(results) == 0:
                insert_sql = "INSERT INTO user (`name`, create_time) VALUES \
                ('%s', %s)" % (item['name'], item['create_time'])
                self.cursor.execute(insert_sql)
                uid = int(self.cursor.lastrowid)
                self.db.commit()
            else:
                uid = results[0][0]
            self.insert_user_star_project(uid, item['pid'])

        # print(item)

    def insert_user_star_project(self, uid, pid):
        if uid and pid:
            select_u2p_sql = "SELECT * FROM user_star_project WHERE uid = %s AND pid = %s" % (uid, pid)
            self.cursor.execute(select_u2p_sql)
            results = self.cursor.fetchall()
            if len(results) == 0:
                insert_sql = "INSERT INTO user_star_project (uid, pid) VALUES ('%s', '%s')" % (uid, pid)
                self.cursor.execute(insert_sql)
                self.db.commit()

    def handle_user_detail(self, item):
        if item:
            update_sql = "UPDATE `user` SET repositories=%s, stars=%s, follows=%s, following=%s WHERE id=%s" \
                         % (item['repositories'], item['stars'], item['follows'], item['following'], item['id'])
            self.cursor.execute(update_sql)
            self.db.commit()


