from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(t.`year`) as year
                        from lahmansbaseballdb.teams t 
                        where t.`year` >= 1980 """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getTeams(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(t.teamCode) as teamCode, t.name, sum(s.salary) salaries
                        from lahmansbaseballdb.teams t, lahmansbaseballdb.salaries s 
                        where t.`year` = %s
                                and t.teamCode = s.teamCode
                                and t.`year` = s.`year` 
                        group by t.teamCode """
            cursor.execute(query, (year, ))

            for row in cursor:
                result.append(Team(row["teamCode"], row["name"], int(row["salaries"])))
                print(row["teamCode"], row["name"], row["salaries"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t.teamCode as one, t2.teamCode as two 
                        from lahmansbaseballdb.teams t, lahmansbaseballdb.teams t2, lahmansbaseballdb.salaries s , lahmansbaseballdb.salaries s2
                        where t.`year` = %s
                                and s.ID = t.ID
                                and s2.ID = t2.ID
                                and t.`year` = t2.`year`
                                and t.teamCode <> t2.teamCode 
                                and t.ID > t2.ID """
            cursor.execute(query, (year,))

            for row in cursor:
                result.append((row["one"], row["two"]))
            cursor.close()
            cnx.close()
        return result



