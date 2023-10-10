import pandas as pd
import psycopg2
import requests
from psycopg2 import pool

class AlerceDataBaseHandler:
    
    connection_pool = None


    def __init__(self):
        """
        Constructor: Inicializa el pool de conexiones a la base de datos.
        """
        if not self.connection_pool:
            self.initialize_connection_pool()

    @classmethod
    def initialize_connection_pool(self):
        # Create a connections pool with a min and max connections
        url = "https://raw.githubusercontent.com/alercebroker/usecases/master/alercereaduser_v4.json"
        params = requests.get(url).json()["params"]
        pool_min_connections = 1
        pool_max_connections = 10
        print("[INFO] create ALeRCE pool connection")
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                pool_min_connections, 
                pool_max_connections, 
                dbname=params["dbname"],
                user=params["user"],
                host=params["host"],
                password=params["password"])
        except BaseException as e:
            print(f"[ERROR] when create a pool connection {e}")
        else:
            print("[INFO] Pool create!")
            print(type(self.connection_pool))
        
    @classmethod
    def close_connection_pool(self):
        """
        Cierra el pool de conexiones a la base de datos.
        """
        if self.connection_pool:
            self.connection_pool.closeall()
            self.connection_pool = None
    

    def __del__(self):
        """
        Destructor: Cierra el pool de conexiones a la base de datos.
        """
        self.close_connection_pool()

    @staticmethod
    def query_data(query):
        """
        Executes a SQL query on the connected database.

        Args:
            query (str): SQL query to be executed.

        Returns:
            pd.DataFrame: Dataframe containing the result of the query.
        """ 
        try:

            print("[INFO] get pool connection to Alerce")
            print(type(AlerceDataBaseHandler.connection_pool))
            conn=AlerceDataBaseHandler.connection_pool.getconn()
            
            print("[INFO] query to Alerce")
            print(f"[INFO] {query}")
            query_dataframe = pd.read_sql_query(query, conn)
            
            query_dataframe = query_dataframe.loc[:, ~query_dataframe.columns.duplicated()].copy()
        except BaseException as e:
            
            print("[INFO] close pool connection to Alerce")
            AlerceDataBaseHandler.connection_pool.putconn(conn)
            print(f"[Error] {e}")
            return pd.DataFrame()
        else:
            print("[INFO] close pool connection to Alerce")
            AlerceDataBaseHandler.connection_pool.putconn(conn)
            print("[INFO] query successful!")
            return query_dataframe


    @staticmethod
    def fetch_object_basic(oid):
        """
        Fetch basic information for a specific object.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframe containing basic information.
        """
        try:
            basic_info_obj = AlerceDataBaseHandler.query_data(
                """
                SELECT 
                    o.oid, 
                    o.firstmjd, 
                    o.lastmjd, 
                    o.stellar, 
                    o.corrected,
                    (SELECT 
                        COUNT(*) 
                        FROM 
                            detection AS d 
                        WHERE o.oid = d.oid) AS det
                    ,
                    (SELECT 
                        COUNT(*) 
                        FROM non_detection AS nd 
                        WHERE o.oid = nd.oid) AS non_det

                FROM object AS o
                WHERE o.oid = '%s'

                """ % (oid)
            )

            return basic_info_obj
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    @staticmethod
    def fetch_objects_location(oid):
        """
        Fetch location information for a specific object.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframe containing location information.
        """
        try:
            obj_location = AlerceDataBaseHandler.query_data(
                """
                SELECT 
                    o.oid, 
                    o.meanra,
                    o.meandec
                FROM object AS o
                WHERE o.oid= '%s'
                """ % (oid)
            )
            return obj_location
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    @staticmethod
    def fetch_objects_complete(model_name, count_limit, probability_upper_limit):
        """
        Fetch complete information for objects based on specific criteria.

        Args:
            model_name (str): The name of the model.
            count_limit (int): The limit of objects to fetch.
            probability_upper_limit (float): The probability upper limit.

        Returns:
            pd.DataFrame: Dataframe containing complete information for objects.
        """
        try:
            basic_info_obj = AlerceDataBaseHandler.query_data(
                """
                SELECT 
                    o.oid, 
                    o.firstmjd, 
                    o.lastmjd, 
                    o.stellar, 
                    o.corrected,
                    (SELECT 
                        COUNT(*) 
                        FROM 
                            detection AS d 
                        WHERE o.oid = d.oid) AS det,
                    (SELECT 
                        COUNT(*) 
                        FROM non_detection AS nd 
                        WHERE o.oid = nd.oid) AS non_det,
                    o.meanra,
                    o.meandec
                FROM object AS o
                WHERE o.oid 
                    IN (
                        SELECT 
                            p.oid 
                        FROM probability AS p
                        WHERE 
                            p.classifier_name = '%s' 
                            AND 
                            p.probability > %f
                    )
                ORDER BY oid DESC
                LIMIT %d;

                """ % (model_name, probability_upper_limit, count_limit)
            )

            return basic_info_obj
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    @staticmethod
    def fetch_lc_data(oid):
        """
        Fetch light curve data for a specific object.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframes containing detection and non-detection data.
        """
        try:
            det = AlerceDataBaseHandler.query_data(
                '''
                SELECT
                    *
                FROM
                    detection
                WHERE
                    oid = '%s'
                ''' % oid
            )
            print("-" * 20)
            print(det.head())
            print("-" * 20)
            non_det = AlerceDataBaseHandler.query_data(
                '''
                SELECT
                    *
                FROM
                    non_detection
                WHERE
                    oid = '%s'
                ''' % oid
            )

            return det, non_det
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame(), pd.DataFrame()

    @staticmethod
    def fetch_lc_magstat(oid):
        """
        Fetch magnitude statistics for a specific object's light curve.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframe containing magnitude statistics.
        """
        # 1:g, 2:r 
        try:
            magstatG = AlerceDataBaseHandler.query_data(
                '''
                SELECT
                    m.oid,
                    m.ndubious,
                    m.magmean,
                    m.magmedian,
                    m.magmax,
                    m.magmin,
                    m.magsigma,
                    m.maglast,
                    m.magfirst,
                    m.firstmjd,
                    m.lastmjd,
                    m.step_id_corr
                FROM
                    magstat as m
                WHERE
                    oid = '%s' and fid=1
                ''' % oid
            )
            magstatR = AlerceDataBaseHandler.query_data(
                '''
                SELECT
                    m.oid,
                    m.ndubious,
                    m.magmean,
                    m.magmedian,
                    m.magmax,
                    m.magmin,
                    m.magsigma,
                    m.maglast,
                    m.magfirst,
                    m.firstmjd,
                    m.lastmjd,
                    m.step_id_corr
                FROM
                    magstat as m
                WHERE
                    oid = '%s' and fid=2
                ''' % oid
            )
            return magstatG,magstatR
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()

    @staticmethod
    def fetch_probability(oid):
        """
        Fetch class probability for a specific object.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframe containing class probabilities.
        """
        try:
            probability = AlerceDataBaseHandler.query_data(
                '''
                SELECT
                    p.oid,p.class_name,p.probability
                FROM
                    probability as p
                WHERE
                    oid = '%s'
                ORDER BY probability DESC
                ''' % oid
            )

            probability['class_name'] = probability['class_name'].str.strip()
            probability = probability.drop_duplicates(subset=['class_name'])

            columns = ["AGN", "SNII", "SNIa", "CEP", "RRL", "DSCT", "E", "LPV", "YSO", "SLSN", "QSO", "Blazar", "CV/Nova", "SNIbc", "Periodic-Other"]
            probability = probability[probability['class_name'].isin(columns)]
            probability = probability.reset_index(drop=True)

            return probability
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()
        
    @staticmethod
    def fetch_period(oid):
        """
        Fetch class probability for a specific object.

        Args:
            oid (str): The object ID.

        Returns:
            pd.DataFrame: Dataframe containing class probabilities.
        """
        try:
            period = AlerceDataBaseHandler.query_data(
                '''
                select oid, name, value from feature where name = 'Multiband_period' and oid ='%s'
                    
                ''' % oid
            )
            print("*"*20)
            print(period)
            #period.to_csv("out.csv'")

            print("*"*20)
            
            if len(period) > 0:
                period = float(period.value.values[0])
            
            print("?"*20)
            
            print(period)

            print("?"*20)
            return period
        except BaseException as e:
            print(f"[ERROR] {e}")
            return pd.DataFrame()
