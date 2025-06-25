from database.DB_connect import DBConnect
from model.edges import Edge
from model.nodes import Node


class DAO():
    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.datetime) as y
from sighting s
order by y desc"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["y"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from sighting s 
where s.shape = %s and year(s.datetime) = %s
order by s.shape asc"""
        cursor.execute(query, (shape, year,))

        for row in cursor:
            result.append(Node(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(year, shape, idNodes):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as n1, t2.id as n2, t2.longitude-t1.longitude as weight
from
(select id, state, longitude 
from sighting s 
where s.shape = %s and year(s.datetime) = %s
order by s.shape asc) t1,
(select id, state, longitude 
from sighting s 
where s.shape = %s and year(s.datetime) = %s
order by s.shape asc) t2
where t1.state = t2.state
and t1.id <> t2.id
and t1.longitude < t2.longitude"""
        cursor.execute(query, (shape, year, shape, year, ))

        for row in cursor:
            result.append(Edge(idNodes[row['n1']], idNodes[row['n2']], row['weight']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape as s
from sighting
where shape <> "" and year(datetime) = %s
order by shape asc"""
        cursor.execute(query, (year, ))

        for row in cursor:
            result.append(row["s"])
        cursor.close()
        conn.close()
        return result