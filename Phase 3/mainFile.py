import csv
import sys
import math
import datetime
import numpy as np
import random
import os.path
import xml.dom.minidom
from sklearn.preprocessing import normalize
import webbrowser
import gc
from fnmatch import fnmatch
import glob
import shutil
import pickle
import matplotlib.pyplot as plt
import networkx as nx
import numpy
from scipy.spatial import distance
from tempfile import TemporaryFile
import operator
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity as cosineSimilarity
from sklearn.metrics.pairwise import euclidean_distances as euclideanDistance
from sklearn.metrics.pairwise import manhattan_distances as manhattanDistance

# class Graph:
#
#     def __init__(self, graph):
#         self.graph = graph  # residual graph
#         self.org_graph = [i[:] for i in graph]
#         self.ROW = len(graph)
#         self.COL = len(graph[0])
#
#     '''Returns true if there is a path from source 's' to sink 't' in
#     residual graph. Also fills parent[] to store the path '''
#
#     def BFS(self, s, t, parent):
#
#         # Mark all the vertices as not visited
#         visited = [False] * (self.ROW)
#
#         # Create a queue for BFS
#         queue = []
#
#         # Mark the source node as visited and enqueue it
#         queue.append(s)
#         visited[s] = True
#
#         # Standard BFS Loop
#         while queue:
#
#             # Dequeue a vertex from queue and print it
#             u = queue.pop(0)
#
#             # Get all adjacent vertices of the dequeued vertex u
#             # If a adjacent has not been visited, then mark it
#             # visited and enqueue it
#             for ind, val in enumerate(self.graph[u]):
#                 if visited[ind] == False and val > 0:
#                     queue.append(ind)
#                     visited[ind] = True
#                     parent[ind] = u
#
#                     # If we reached sink in BFS starting from source, then return
#         # true, else false
#         return True if visited[t] else False
#
#     # Returns the min-cut of the given graph
#     def minCut(self, source, sink):
#
#         # This array is filled by BFS and to store path
#         parent = [-1] * (self.ROW)
#
#         max_flow = 0  # There is no flow initially
#
#         # Augment the flow while there is path from source to sink
#         while self.BFS(source, sink, parent):
#
#             # Find minimum residual capacity of the edges along the
#             # path filled by BFS. Or we can say find the maximum flow
#             # through the path found.
#             path_flow = float("Inf")
#             s = sink
#             while (s != source):
#                 path_flow = min(path_flow, self.graph[parent[s]][s])
#                 s = parent[s]
#
#                 # Add path flow to overall flow
#             max_flow += path_flow
#
#             # update residual capacities of the edges and reverse edges
#             # along the path
#             v = sink
#             while (v != source):
#                 u = parent[v]
#                 self.graph[u][v] -= path_flow
#                 self.graph[v][u] += path_flow
#                 v = parent[v]
#
#                 # print the edges which initially had weights
#         # but now have 0 weight
#         for i in range(self.ROW):
#             for j in range(self.COL):
#                 if self.graph[i][j] == 0 and self.org_graph[i][j] > 0:
#                     print
#                     str(i) + " - " + str(j)

# def returnUserTerms(row):
#     col_count = 1
#     tempTermArray = []
#     while col_count < len(row):
#         tempTermArray.append(row[col_count])
#         col_count += 4
#     tempTermArray.pop()
#     return tempTermArray

def getCSVDataAsListData(fileName):
        mainData = []
        with open(fileName) as csv_file:
            csvData = csv.reader(csv_file, delimiter=',')
            for row in csvData:
                mainData.append(row)
            return mainData

# def returnUserTfValues(row):
#     col_count = 2
#     tempTermArray = []
#     while col_count < len(row):
#         tempTermArray.append((int)(row[col_count]))
#         col_count += 4
#     return tempTermArray
#
# def returnUserDfValues(row):
#         col_count = 3
#         tempTermArray = []
#         while col_count < len(row):
#             tempTermArray.append(row[col_count])
#             col_count += 4
#         return tempTermArray
#
# def returnUserTfIdfValues(row):
#         col_count = 4
#         tempTermArray = []
#         while col_count < len(row):
#             tempTermArray.append(row[col_count])
#             col_count += 4
#         return tempTermArray

# def getAllImagesTermDict(fileName):
#     allImageTermDict={}
#     allImageData = getCSVDataAsListData(fileName)
#     for row in allImageData:
#         terms = returnUserTerms(row)
#         allImageTermDict[row[0]] = terms
#     return allImageTermDict
#
# def getAllImagesTFDict(fileName):
#     allImageTFDict={}
#     allImageData = getCSVDataAsListData(fileName)
#     for row in allImageData:
#         terms = returnUserTfValues(row)
#         allImageTFDict[row[0]] = terms
#     return allImageTFDict

def createDict(mainTermArr,mainTFValues):
    dict={}
    for idx,term in enumerate(mainTermArr):
        dict[term] = mainTFValues[idx]
    return dict

def findSimilarityScoreBetweenImages(mainDict,otherDict):
    score = 0
    for key in mainDict:
        if key in otherDict:
            score = score + abs(mainDict[key]-otherDict[key])
        else:
            score = score + abs(mainDict[key])
    #all(map(mainDict.pop, otherDict))
    for key in otherDict:
        if key not in mainDict:
            score = score +abs(otherDict[key])
    return score

def findSimilarityScoreBetweenImagesUsingL2(mainDict,otherDict):
    score = 0
    for key in mainDict:
        if key in otherDict:
            score = score + pow(mainDict[key]-otherDict[key],2)
        else:
            score = score + pow(mainDict[key],2)
    #all(map(mainDict.pop, otherDict))
    for key in otherDict:
        if key not in mainDict:
            score = score +pow(otherDict[key],2)
    return math.sqrt(score)


#get 5 most similar images to given image.
def getKMostSimilarImagesAndScores(scoreArr,k):
    a = np.asarray(scoreArr)
    #imageIDArray = np.asarray(allImageIDs)
    imageIDArray = np.asarray(allImageIDs)
    idx = np.argpartition(a, k)
    #keys = list(imageTermDict.keys())
    imageIDs = imageIDArray[idx[:k]]
    scores = scoreArr[idx[:k]]
    return imageIDs,scoreArr

def getKMostSimilarImagesAndScoresAsDict(scoreArr,k):
    a = np.asarray(scoreArr)
    idx = np.argpartition(a, k)
    tmpArr = np.asarray(allImageIDs)
    imageIDs = tmpArr[idx[:k]]
    scores = scoreArr[idx[:k]]
    tempDict={}
    for idx,imageid in enumerate(imageIDs):
        tempDict[imageid] = scores[idx]
    return tempDict

def getAllSimilarImagesAndScoresAsDict(scoreArr):
    tempDict={}
    for idx,imageid in enumerate(allImageIDs):
        tempDict[imageid] = scoreArr[idx]
    return tempDict

def printAndSaveGraphProperly(grph,name):
    with open(name, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in grph.items()]

# def createClusterDict(listofclusters):
#     clusterDict = {}
#     for centroid in listofclusters:
#         tempDict = {}
#         clusterDict[centroid] = tempDict
#     for key in outputDict:
#         minDistance = 999999999
#         closestClusterCentroid = ""
#         for centroid in listofclusters:
#             if outputDict[key][centroid]:
#                 if minDistance > outputDict[key][centroid]:
#                     minDistance = outputDict[key][centroid]
#                     closestClusterCentroid = centroid
#             #else:
#
#         clusterDict[closestClusterCentroid][key] = outputDict[key][closestClusterCentroid]
#     return clusterDict

# def getAllUniqueTerms(fileName):
#     allImageData = getCSVDataAsListData(fileName)
#     allterms=[]
#     for row in allImageData:
#         imageIDList.append(row[0])
#         allterms.extend(returnUserTerms(row))
#     return set(allterms)

def assign_clusters(current_centroids):
        res_dist = distance.cdist(imageImageSparse, current_centroids, metric='euclidean')
        assigned_cluster = np.array([list(each).index(min(each)) for each in res_dist])
        return assigned_cluster

def compute_centroid(previous_centroids, clusters):
        new_centroids = np.zeros(previous_centroids.shape)
        for i in range(len(previous_centroids)):
            current_cluster_indices = np.where(clusters==i)
            current_cluster = imageImageSparse[current_cluster_indices]
            new_centroids[i] = np.mean(current_cluster, axis=0)
        return new_centroids

def getRandomCentroids(c) :
    clusterCentroids = []
    clusterIDs = random.sample(list(outputDict.keys()), c)
    for idx, clusterid in enumerate(clusterIDs):
        keys = list(outputDict.keys())
        indx = keys.index(clusterid)
        clusterCentroids.append(imageImageSparse[indx])
    return np.matrix(clusterCentroids),clusterIDs

def drawGraph(G):

    print (len(G.nodes))
    print(" drawing graph")
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'))
    #nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='b', arrows=True)
    print(" showing graph")
    plt.show()

def createGraphFromClusterArr(clusterArr,clusterIDs) :
    G = nx.DiGraph()
    print("creating graph")
    for idx, val in enumerate(clusterArr):
        col = allImageIDs.index(clusterIDs[val])
        G.add_edge(clusterIDs[val], allImageIDs[idx], capacity=imageImageSparse[idx][col])
    print(" graph created")
    drawGraph(G)

def copyFiles(filename) :
    for path, subdirs, files in os.walk("./data/images/"):
        for name in files:
            if (filename in name):
                #print("match")
                #shutil.copy(os.path.join(path, name), dirname)
                return os.path.join(path, name)

def showImagesInWebPage(clusterDict,webpagename,showClusterName):
    print("\n Creating Web Page")
    f = open(webpagename, 'w')
    message = """<html><head></head><body>"""
    f.write(message)
    # add html code here
    content = """<table><tbody>"""
    for idx,key in enumerate(clusterDict):
        if not showClusterName :
            content = content + """<tr><td><H1>Cluster """ + str(idx) + """</H1></td></tr><tr>"""
        else:
            content = content + """<tr><td><H1>""" + str(key) + """</H1></td></tr><tr>"""
        for idx, image in enumerate(clusterDict[key]):
            if not image == None and ".jpg" in image:
                content = content + """<td><img src=\"""" + image + """\" height="100" width="100"></td>"""
        content = content + """</tr>"""

    content = content + """</tbody></table>"""
    f.write(content)
    f.write("""</body></html>""")
    f.close()
    filename = 'file:///Users/sumeetbhalla/PycharmProjects/mwdbphase3/' + webpagename
    webbrowser.open_new_tab(filename)


def splitImagesInClusters(clusterArr,clusterIDs) :
    #create folders with cluster numbers
    for id in range(len(clusterIDs)):
        #os.mkdir(id)
        clusterDict[id] = []
    print("\n Creating Cluster Dict with Image Paths")
    for idx, val in enumerate(clusterArr):
        #if len(clusterDict[clusterIDs[val]]) != 0:
        clusterDict[val].append(copyFiles(allImageIDs[idx]+".jpg"))
        print("created paths for " + str(val))
        #else:
            # indexOfImage = allImageIDs.index(clusterIDs[val])
            # getKMostSimilarImagesAndScores(similarityMatrix)
            # clusterDict[clusterIDs[val]].append
    count = np.zeros(len(clusterIDs))
    for idx, val in enumerate(clusterArr):
        count[val] = count[val]+1
    print ("cluster images inside each cluster")
    for val in count:
        print (val)

        #copyFiles(allImageIDs[idx]+".jpg",clusterIDs[val])
    #print(clusterDict)1

    #printAndSaveGraphProperly(clusterDict,"KMeansDict.csv")
    #pickling_on = open("kMeansDict.pickle", "wb")
    #pickle.dump(clusterDict, pickling_on)
    #pickling_on.close()


    showImagesInWebPage(clusterDict,'kmeansoutput.html',False)


def trigger_k_means(c):
    current_centroids,clusterIDs = getRandomCentroids(c)
    previous_centroids = []
    counter = 0
    while not np.array_equal(previous_centroids, current_centroids) and counter < 20:
        assigned_clusters = assign_clusters(current_centroids)
        previous_centroids = current_centroids
        current_centroids = compute_centroid(previous_centroids, assigned_clusters)
        counter = counter+1
        #potential_func_value = self.calculate_potential_function(current_centroids, assigned_clusters)
        print("iteration "+str(counter))
    print("custers created")
    return assigned_clusters,clusterIDs

def createAllModelMatrix(targetFileNames):
    finalVector = []
    for x, file in enumerate(targetFileNames):
        filedata = getCSVDataAsListData(file)
        fileDataNP = np.asarray(filedata)
        deletedArr = np.delete(fileDataNP,[0],axis=1)
        if len(finalVector) == 0:
            finalVector = deletedArr
        else:
            finalVector = np.append(finalVector,deletedArr, axis=1)
    return  normalize(np.asfarray(finalVector, float)), fileDataNP[:,0]


def loadDataset(filename, trainingSet={}):
    with open(filename) as f:
        for line in f:
            s = line.strip().split(" ")
            trainingSet[(s[0])] = s[1].strip()

startTime = datetime.datetime.now()
allImageIDs = []
#using visual descriptors
fileName = ''
locationName = ""
otherLocationNames=[]
targetFileNames = []
fileNamesToCompare = []
doc = xml.dom.minidom.parse("./data/devset_topics.xml")
titles = doc.getElementsByTagName('title')
indexes = doc.getElementsByTagName('number')

for i in range(len(indexes)):
    otherLocationNames.append(titles[i].firstChild.data)

#print ("Target Location Name = "+str(locationName))
#print "Other Location Names = "+ str(otherLocationNames)
for file in os.listdir("./data/img/"):
    #if locationName in file:
    #    targetFileNames.append("./data/img/"+file)
    fileNamesToCompare.append("./data/img/"+file)

print ("Location names to compare = "+str(len(fileNamesToCompare)))

#calculate the file clusters for each location
otherLocationFileCluster = []
for idx,location in enumerate(otherLocationNames):
    tempCluster=[]
    for idy,fileName in enumerate(fileNamesToCompare):
        if location in fileName:
            tempCluster.append(fileName)
    otherLocationFileCluster.append(tempCluster)

print ("No of locations to compare = "+str(len(otherLocationFileCluster)) +" with "+str(len(otherLocationFileCluster[0]))+"files for each location")


#allModalArray = createAllModelMatrix(targetFileNames)
finalImageFeatureMatrix =[]
for idx, fileCluster in enumerate(otherLocationFileCluster):
    allModalArray,imageIdArr = createAllModelMatrix(fileCluster)
    if len(finalImageFeatureMatrix) == 0:
        finalImageFeatureMatrix = allModalArray
        allImageIDs.extend(imageIdArr)
    else:
        finalImageFeatureMatrix = np.append(finalImageFeatureMatrix, allModalArray, axis=0)
        allImageIDs.extend(imageIdArr)

count=0;
print("\nAll Image Featur Matrix Created")
print ("Total Time taken to Execute")
print (str(datetime.datetime.now()-startTime))
startTime = datetime.datetime.now()

similarityfileexists = os.path.isfile("similaritymatrix.npy")
if not similarityfileexists:
    similarityMatrix = euclideanDistance(finalImageFeatureMatrix)
    # similarityMatrix = cosineSimilarity(finalImageFeatureMatrix)
    # similarityMatrix = manhattanDistance(finalImageFeatureMatrix)
    numpy.save("similaritymatrix", similarityMatrix)
else:
    similarityMatrix = numpy.load("similaritymatrix.npy")

print("\nEuclidian similarty done/loaded")
print ("Total Time taken to Execute")
print (str(datetime.datetime.now()-startTime))
startTime = datetime.datetime.now()

outputDict={}
G = nx.DiGraph()
taskNumber = (int)(input("Enter task number = "))
while taskNumber>0:

    if taskNumber == 1:
        task1output = os.path.isfile("task1output.pickle")
        if not task1output:
            k = (int)(input("Enter value for K = "))
            #calculating most similar k values for each image

            for idx,row in enumerate(similarityMatrix):
                outputDict[allImageIDs[idx]] = getKMostSimilarImagesAndScoresAsDict(row,k)
                imageIDs,scoreIDs = getKMostSimilarImagesAndScores(row,k)
                for idx,imageID in enumerate(imageIDs):
                    G.add_edge(allImageIDs[idx], imageID, capacity=scoreIDs[idx])
            printAndSaveGraphProperly(outputDict,"task1-output.csv")
            pickling_on = open("task1output.pickle", "wb")
            pickle.dump(outputDict, pickling_on)
            pickling_on.close()
        else:
            outputDict = pickle.load(open("task1output.pickle", "rb"))

        print ("\nTask 1 complete")
        print ("Total Time taken to Execute")
        print (str(datetime.datetime.now()-startTime))

    elif taskNumber == 2:
        print("\nTask 2:\n")
        c = (int)(input("Enter number of Clusters c = "))
        #creating a sparse matrix using the task 1 reduced graph
        task2choice = (int)(input("\nEnter 1 - K Means or 2 - Spectral Clustering - "))
        if task2choice == 1:
            imageImageSparse = numpy.zeros(similarityMatrix.shape)
            for idx, key1 in enumerate(outputDict):
                tempDict = outputDict[key1]
                for idy,key2 in enumerate(tempDict):
                    col = allImageIDs.index(key2)
                    imageImageSparse[idx][col] = tempDict[key2]

            imageImageSparse = similarityMatrix
            allClustersArr,clusterIDs = trigger_k_means(c)

            print("\nK-Means clustering done")
            print("Total Time taken to Execute")
            print(str(datetime.datetime.now() - startTime))
            startTime = datetime.datetime.now()

            clusterDict={}
            splitImagesInClusters(allClustersArr,clusterIDs)
            print("\nCreating Output Dict and Showing web page done")
            print("Total Time taken to Execute")
            print(str(datetime.datetime.now() - startTime))
            startTime = datetime.datetime.now()
        if task2choice == 2:
            print("\n Spectral Clustering Code Here")

    elif taskNumber == 3:
        print("Task 3 code here")
        print("\nTask 3:\n")

    elif taskNumber == 4:
        print("Task 4 code here")
        print("\nTask 4:\n")

    elif taskNumber == 5:
        print("Task 5 code here")
        print("\nTask 5:\n")

    elif taskNumber == 6:
        print("\nTask 6:\n")
        task6choice = (int)(input("\nEnter 1 - KNN or 2 - PPR based classiciation - "))
        if task6choice == 1:
            trainingSet = {}
            loadDataset("./data/task6-testsample.txt", trainingSet)
            labelled_dic_all_images = {}
            # print(len(allImageIDs))
            # print(similarityMatrix.shape)
            uniqueLabels = []
            allLables = []
            for key, val in trainingSet.items():
                if val not in uniqueLabels:
                    uniqueLabels.append(val)
                allLables.append(val)

            for label in uniqueLabels:
                labelled_dic_all_images[label] = []
            loadDataset("./data/task6-testsample.txt", trainingSet)
            k = (int)(input("enter value for k = "))
            for idx, img in enumerate(allImageIDs):
                minscore = 999
                minlabel = ""
                labelScoreArr = []
                #print("Training Set items")
                #print(trainingSet.items())
                for key, val in trainingSet.items():
                    # print(key,val)
                    # minlabel = trainingSet[key]
                    imgid = key
                    # print(allimgi)
                    # print(len(allImageIDs))

                    if (imgid in allImageIDs):
                        #print("match " + imgid)
                        minindex = allImageIDs.index(imgid)
                        currentscore = similarityMatrix[idx][minindex]
                        labelScoreArr.append(currentscore)
                        # if currentscore <= minscore:
                        #     minscore = currentscore
                        #     minlabel = trainingSet[key]
                    else:
                        print("no match " + imgid)
                # find indexes of k smallest values
                #print(len(labelScoreArr))

                labelArr = np.asarray(labelScoreArr)
                idx = np.argpartition(labelArr, k)
                alllabelArr = np.asarray(allLables)
                labels = alllabelArr[idx[:k]]
                #print("Top K labels")
                #print(labels)
                labels, counts = np.unique(labels, return_counts=True)
                #print("Unique labels")
                #print(labels)
                #print("Unique counts")
                #print(counts)
                tempCounts = counts.tolist()
                minlabel = labels[tempCounts.index(max(counts))]

                labelled_dic_all_images[minlabel].append(img)
                # minscore = similarityMatrix[img][minindex]
            # print (labelled_dic_all_images)
            printAndSaveGraphProperly(labelled_dic_all_images, "KNN-Output.csv")
            task6ClusterDict={}
            for id in labelled_dic_all_images:
                # os.mkdir(id)
                task6ClusterDict[id] = []
            print("\n Creating Cluster Dict with Image Paths")
            for key, value in labelled_dic_all_images.items():
                for imageID in value:
                    task6ClusterDict[key].append(copyFiles(imageID + ".jpg"))
                print("created paths for "+str(key))
            showImagesInWebPage(task6ClusterDict,'task6output.html',True)
        if task6choice == 2:
            print("\nPPR based classification implementation code here")
    taskNumber = (int)(input("Enter task number = "))