import csv
from py2neo import Graph, Node, Relationship
import tqdm

# /var/lib/neo4j/import

if __name__ == "__main__":
    graph = Graph("bolt://127.0.0.1:7687", username="neo4j", password="root")
    graph.run('MATCH ()-[r:HasSpeaker]->() DELETE r')
    graph.run('MATCH ()-[r:HasTrack]->() DELETE r')
    graph.run('MATCH (n:Title) DELETE n')
    graph.run('MATCH (n:Title) DELETE n')
    graph.run('MATCH (n:Speaker) DELETE n')
    graph.run('MATCH (n:Track) DELETE n')
    
    with open('blackhat2019.csv', 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp)
        header = next(reader)
        for row in tqdm.tqdm(reader):
            title, speakers, tracks, url = row
            graph.run('MERGE (:Title {name:"' + title + '", url:"' + url + '"})')
            for speaker in speakers.split(','):
                tmp = speaker.replace('"', '')
                graph.run('MERGE (:Speaker {name:"' + tmp + '"})')
                graph.run('MATCH (t:Title {name:"' + title + '"}), (s:Speaker {name:"' + tmp + '"}) CREATE (t)-[:HasSpeaker]->(s)')
            for track in tracks.split(','):
                graph.run('MERGE (:Track {name:"' + track + '"})')
                graph.run('MATCH (ti:Title {name:"' + title + '"}), (tr:Track {name:"' + track + '"}) CREATE (ti)-[:HasTrack]->(tr)')

    graph.run('CREATE CONSTRAINT ON (b:Title) ASSERT b.name IS UNIQUE')