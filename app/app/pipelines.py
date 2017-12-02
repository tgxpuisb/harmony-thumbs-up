# -*- coding: utf-8 -*-
import pymysql



class AppPipeline(object):

    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', 'assassin12', 'github')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):

        if spider.name == 'project':
            self.handle_project(item)
        return item

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
        pass

