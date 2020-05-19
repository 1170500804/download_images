"""
/*------------------------------------------------------*
|  This script downloads images from google API         |
|                                                       |
| Author: Charles Wang,  UC Berkeley c_w@berkeley.edu   |
|                                                       |
| Date:    07/15/2019                                   |
*------------------------------------------------------*/
"""


import os
import requests 
import random
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

def generate_dir(to_generate):
    images = os.path.join(os.getcwd(), 'occupancy_images')
    if not os.path.exists(images):
        os.mkdir(images)
    for f in to_generate:
        cur_dir = os.path.join(images, f)
        if not os.path.exists(cur_dir):
            os.mkdir(cur_dir)

def  download(urls):
    """Function to download images using Google API.
    
    Args:
        urls (List): [[urlTop,urlStreet,lon,lat,BldgID],...]
    """
    for ls in urls:
        #urlTop = ls[0]
        urlStreet = ls[0]
        lon = ls[1]
        lat = ls[2]
        osmID = ls[3]
        file = ls[4]
        resolution = ls[5]
        fov = ls[6]

#         roofPicName = outputDir + '/{BldgID}-{prefix}.png'.format(BldgID=BldgID,prefix='TopView')
#         if not os.path.exists(roofPicName):
#             print(urlTop)
#             r = requests.get(urlTop)
#             f = open(roofPicName, 'wb')
#             f.write(r.content)
#             f.close()

        streetPicName = outputDir + '/'+file+'/{osmID}-{prefix}-{resolution}-{fov}.jpg'.format(osmID=int(osmID),prefix='StreetView',resolution=str(resolution),fov=str(fov))
        if not os.path.exists(streetPicName):
            print(urlStreet)
            r = requests.get(urlStreet)
            f = open(streetPicName, 'wb')
            f.write(r.content)
            f.close()

def get_pics(dictFile, filename,resolution,fov):
    urls = []
    for index, row in dictFile.iterrows():
        osmID = row['osm_id']
        lat = row['latitude']
        lon = row['longitude']
        #StructureUse = row['StructureUse']

        #urlTop = baseurl_satellite.format(lat=lat,lon=lon)
        urlStreet = baseurl_streetview.format(lat=lat,lon=lon,res = resolution,fov=fov)
        urls.append([urlStreet,lon,lat,osmID,filename,resolution,fov])
    print('shuffling...')
    random.shuffle(urls)
    print('shuffled...')


    # divide urls into small chunks
    ncpu = 1
    step = int(len(urls)/ncpu)+1
    chunks = [urls[x:x+step] for x in range(0, len(urls), step)]


    print('Downloading images from Google API ...')
    # get some workers
    pool = ThreadPool(ncpu)
    # send job to workers
    results = pool.map(download, chunks)
    # jobs are done, clean the site
    pool.close()
    pool.join()
#    map(download, urls)
    print('Images downloaded ...')



if __name__ == '__main__':

    GoogleMapAPIKey = "AIzaSyDl14FuoXEHzqn22HahVAER8SlZNCjwEjI"
    test_path = '/Users/liushuai/Documents/Research/RoofMaterial/occupancy/house_xaaaa.csv'
    outputDir = os.path.join(os.getcwd(),'occupancy_images')
    to_download = ["house_xaaaa","residential","detached","apartments","garage","commercial","industrial","office","hotel","hospital","roof","church","terrace","retail","static_caravan","warehouse","school","university","shed"]
    csv_path = os.path.join(os.getcwd(), 'csv/')
    # APIs. notice: you can change pitch and fov to get best capture of the building from the street view. 
    #               zoom and sizes can also be changed.
    baseurl_streetview = "https://maps.googleapis.com/maps/api/streetview?size={res}x{res}&location={lat},{lon}&pitch=0&fov={fov}&key="+GoogleMapAPIKey
    #baseurl_satellite = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=20&scale=1&size=256x256&maptype=satellite&key="+GoogleMapAPIKey+"&format=png&visual_refresh=true"
    # generate output direction
    generate_dir(to_download)
    for d in to_download:
        print('start downloading '+d)
        dictFile = pd.read_csv(os.path.join(csv_path, d+'.csv'))
        get_pics(dictFile, d,640,60)
        print('end downloading ' + d)


