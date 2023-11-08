import base64
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from data.alerce_database_handler import AlerceDataBaseHandler
from models.image.image import Image
from models.magstat.magstat import MagStat
from models.object.object import ObjectBasic, ObjectLocation
from models.lc.lc_det import LightCurveDetection, LightCurveNonDetection, LightCurveData
from services.data_visualizer import DataVisualizer
from matplotlib import pyplot as plt

# Create an APIRouter instance
objects_router = APIRouter()


# Example route to get basic information of an object
@objects_router.get("/basic/{id_objeto}", response_model=ObjectBasic)
async def get_object_basic(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        object_basic = AlerceDataBaseHandler.fetch_object_basic(id_objeto).values.tolist()
        print(object_basic)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        print("[INFO] creating object")
        object = ObjectBasic(
            oid=object_basic[0][0],
            discovery_date=object_basic[0][1],
            last_detection=object_basic[0][2],
            stellar=object_basic[0][3],
            correct=object_basic[0][4],
            det=object_basic[0][5],
            non_det=object_basic[0][6]
        )
        return object

# Example route to get the location of an object
@objects_router.get("/location/{id_objeto}", response_model=ObjectLocation)
async def get_object_location(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        object_location = AlerceDataBaseHandler.fetch_objects_location(id_objeto).values.tolist()
        print(object_location)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        print("[INFO] creating object")
        object = ObjectLocation(
            oid=object_location[0][0],
            ra=object_location[0][1],
            dec=object_location[0][2],
        )
        return object

# Example route to get differential magnitude light curve of an object
@objects_router.get("/dmlc/{id_objeto}", response_model=Image)
async def get_object_diff_mag_lc(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        det, non_det = AlerceDataBaseHandler.fetch_lc_data(id_objeto)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        # Selecciona las columnas necesarias en lc_det
        det = det.loc[:, ['fid', 'mjd', 'magpsf', 'sigmapsf']]


        # Selecciona las columnas necesarias en lc_nondet
        non_det = non_det.loc[:, ['fid', 'mjd', 'diffmaglim']]
        print("[INFO] creating graph")
        print("*"*20)
        print(det)
        print("-"*20)
        print(non_det)
        print("*"*20)
        graph = DataVisualizer.plot_diff_lc(id_objeto, det, non_det)
        encoded_image_string = base64.b64encode(graph)
        return Image(image=encoded_image_string)



# Example route to get differential magnitude light curve of an object
@objects_router.get("/dmlc/info/{id_objeto}", response_model=LightCurveData)
async def get_object_diff_mag_lc_info(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        det, non_det = AlerceDataBaseHandler.fetch_lc_data(id_objeto)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        det = det.loc[:, ['fid', 'mjd', 'magpsf', 'sigmapsf']]
        non_det = non_det.loc[:, ['fid', 'mjd', 'diffmaglim']]




        det_list = [LightCurveDetection(**row) for _, row in det.iterrows()]
        non_det_list = [LightCurveNonDetection(**row) for _, row in non_det.iterrows()]
        
        # Crea y devuelve un objeto LightCurveData con las listas de detecciones y no detecciones
        return LightCurveData(detections=det_list, non_detections=non_det_list)




# Example route to get correlated magnitude light curve of an object
@objects_router.get("/corrlc/{id_objeto}", response_model=Image)
async def get_object_corr_lc(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        det, non_det = AlerceDataBaseHandler.fetch_lc_data(id_objeto)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        print("[INFO] creating graph")
        graph = DataVisualizer.plot_corrLC(id_objeto, det)
        encoded_image_string = base64.b64encode(graph)
        return Image(image=encoded_image_string)

# Example route to get magnitude statistics of an object
@objects_router.get("/magstat/{id_objeto}", response_model=MagStat)#
async def get_object_magstat(id_objeto: str):
    try:
        print("[INFO] request an object from the DB")
        object_magstatG,object_magstatR = AlerceDataBaseHandler.fetch_lc_magstat(id_objeto)
        
        object_magstatG=object_magstatG.values.tolist()
        object_magstatR= object_magstatR.values.tolist()

        print(object_magstatG)
        print(object_magstatR)
    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    else:
        print("[INFO] query successful")
        print("[INFO] creating object")
        
        magStatGR = MagStat(
            oid=object_magstatG[0][0],
            ndubiousG=object_magstatG[0][1],
            magmeanG=object_magstatG[0][2],
            magmedianG=object_magstatG[0][3],
            magmaxG=object_magstatG[0][4],
            magminG=object_magstatG[0][5],
            magsigmaG=object_magstatG[0][6],
            maglastG=object_magstatG[0][7],
            magfirstG=object_magstatG[0][8],
            firstmdjG=object_magstatG[0][9],
            lastmdjG=object_magstatG[0][10],
            step_id_corrG=object_magstatG[0][11],

            ndubiousR=object_magstatR[0][1],
            magmeanR=object_magstatR[0][2],
            magmedianR=object_magstatR[0][3],
            magmaxR=object_magstatR[0][4],
            magminR=object_magstatR[0][5],
            magsigmaR=object_magstatR[0][6],
            maglastR=object_magstatR[0][7],
            magfirstR=object_magstatR[0][8],
            firstmdjR=object_magstatR[0][9],
            lastmdjR=object_magstatR[0][10],
            step_id_corrR=object_magstatR[0][11],
        )
        




        return magStatGR

# Example route to get class probability of an object
@objects_router.get("/probability/{id_objeto}", response_model=Image)
async def get_object_probability(id_objeto: str):
    try:
        probability = AlerceDataBaseHandler.fetch_probability(id_objeto)
        graph = DataVisualizer.radar_chart(probability, id_objeto)
        encoded_image_string = base64.b64encode(graph)
        return Image(image=encoded_image_string)

    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    

@objects_router.get("/folded/{id_objeto}", response_model=Image)
async def get_test(id_objeto: str):
    try:
        period = AlerceDataBaseHandler.fetch_period(id_objeto)
        print(period)
        det, non_det = AlerceDataBaseHandler.fetch_lc_data(id_objeto)
        print(det.head())
        print(non_det.head())
        
        graph =DataVisualizer.plot_folded_light_curve(id_objeto, det, non_det, period)
        encoded_image_string = base64.b64encode(graph)

        return Image(image=encoded_image_string)

    except BaseException as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

