from py2neo import Graph
import matplotlib.pyplot as plt

MARKDOWN = 'blackhat2019.md'

if __name__ == "__main__":
    tracks = []
    counts = []
    graph = Graph("bolt://127.0.0.1:7687", username="neo4j", password="root")
    with open(MARKDOWN, 'w') as fp:
        # All Tracks
        fp.write('# TRACKS\n')
        track_data = graph.run('MATCH () - [:HasTrack] -> (n2) RETURN DISTINCT n2').data()
        for t in track_data:
            t_node = t['n2']
            track = dict(t_node)['name']
            tracks.append(track)
            num_data = graph.run('MATCH (n1) - [:HasTrack] -> (n2:Track {name: "%s"}) RETURN COUNT(n1)' % (track)).data()
            counts.append(int(num_data[0]['COUNT(n1)']))
            fp.write('* %s *%s*\n' % (track, num_data[0]['COUNT(n1)']))

        # All titles
        fp.write('# TITLES\n')
        fp.write('||Titles|Speakers|Tracks|\n')
        fp.write('|-|-|-|-|\n')
        title_data = graph.run('MATCH (n:Title) RETURN n').data()
        for i, t in enumerate(title_data):
            node = t['n']
            title = dict(node)['name']
            url = dict(node)['url']
            
            speaker_data = graph.run('MATCH (n1:Title {name: "%s"}) - [:HasSpeaker] - (n2) RETURN n2' % (title)).data()
            speaker = ''
            for s in speaker_data:
                s_node = s['n2']
                speaker += (dict(s_node)['name'] + ',')
            speaker = speaker[:-2]

            track_data = graph.run('MATCH (n1:Title {name: "%s"}) - [:HasTrack] - (n2) RETURN n2' % (title)).data()
            track = ''
            for t in track_data:
                t_node = t['n2']
                track += (dict(t_node)['name'] + ',')
            track = track[:-2]

            fp.write('|%d|[%s](%s)|%s|%s|\n' % (i + 1, title, url, speaker, track))
            
        # plt
        plt.figure(figsize=(20, 6))
        plt.barh(range(len(tracks)), counts, tick_label=tracks)
        for a, b in zip(range(len(tracks)), counts):
            plt.text(b+0.5, a, b, ha='center', va='center')
        plt.xlabel('Track')
        plt.ylabel('Count')
        plt.savefig('tracks.png')