import igraph as ig
import pandas as pd
import numpy as np
import xnet as xn
import os

MAGColumnTypes = {
	"journal_id": object,
	"issue": object,
	"first_name":object,
	"last_name":object,
	"volume":object,
	"conference_instance_id":object,
	"conference_series_id":object,
	"doc_type":object,
	"doi":object,
	"original_venue":object,
	"publisher":object,
	"authors_last_known_affiliation_id":object,
	"field_of_study_id":object,
	"paper_publisher":object,
	"journal_display_name":object,
	"journal_issn":object,
	"paper_first_page":object,
	"paper_reference_id":object,
	"paper_abstract":object,
}

#def MAGQuery2xnet(queryID):
queryID = "99d71a33-7805-4bff-be2a-8c6c78381688"
nodesData = pd.read_csv("../query-results/%s.csv"%queryID, dtype=MAGColumnTypes)
edgesData = pd.read_csv("../query-results/%s_edges.csv"%queryID)

# Replacing NaN for empty string
for key in MAGColumnTypes:
	if(key in nodesData):
		nodesData[key].fillna("",inplace=True)

# Generating continous indices for papers
index2ID  = nodesData["paper_id"].tolist()
ID2Index = {id:index for index, id in enumerate(index2ID)}

# Hack to account for 2 degree capitalized "FROM"
fromKey = "From";
if(fromKey not in edgesData):
	fromKey = "FROM"

# Converting edges from IDs to new indices
# Invert edges so it means a citation between from to to
edgesZip = zip(edgesData[fromKey].tolist(),edgesData["To"].tolist())
edgesList = [(ID2Index[toID],ID2Index[fromID]) for fromID,toID in edgesZip if fromID in ID2Index and toID in ID2Index]

vertexAttributes = {key:nodesData[key].tolist() for key in nodesData}


for key in nodesData:
	nodesData[key].tolist();

graph = ig.Graph(
	n=len(index2ID),
	edges=edgesList,
	directed=True,
	vertex_attrs=vertexAttributes
);

# verticesToDelete = np.where(np.logical_or(np.array(graph.indegree())==0,np.array(graph.degree())==0))[0]
# graph.delete_vertices(verticesToDelete)

graph.vs["KCore"] = graph.shell_index(mode="IN");
graph.vs["year"] = [int(s[0:4]) for s in graph.vs["date"]];
# graph.vs["Community"] = [str(c) for c in graph.community_infomap().membership];
os.makedirs("../networks", exist_ok=True)
xn.igraph2xnet(graph,"../networks/"+queryID+".xnet")