import json
import requests

if __name__ == "__main__":
    joe_biden_cand_id = 11918
    trump_cand_id = 5
    states = {'Georgia': 'https://embeds.ddhq.io/api/v2/2020general_results/2020general_ga',
    'Nevada': 'https://embeds.ddhq.io/api/v2/2020general_results/2020general_nv',
    'Pennsylvania': 'https://embeds.ddhq.io/api/v2/2020general_results/2020general_pa',
    'Arizona': 'https://embeds.ddhq.io/api/v2/2020general_results/2020general_az',
    'North Carolina': 'https://embeds.ddhq.io/api/v2/2020general_results/2020general_nc'}
    results = {}
    for state, ga_url in states.items():
      results[state] = {}
      results[state]['ddhqRawDataUrl'] = ga_url
      ga_results = json.loads(requests.get(ga_url).text)
      leaders = {}
      estimated_votes = {}
      for entry in ga_results['data']:
        race_id = entry['race_id']
        candidates = entry['candidates']
        if trump_cand_id not in [cand['cand_id'] for cand in candidates]:
          next
        else:
          last_update = entry['last_updated']
          topline_results = entry['toplineResults']
          estimated_votes = topline_results['estimated_votes']
          for can in candidates:
            cand_id = can['cand_id']
            if (cand_id == joe_biden_cand_id or cand_id == trump_cand_id):
              last_name = can['last_name']
              candidate_votes = topline_results['votes'].get(str(can['cand_id']))
              leaders[last_name] = candidate_votes
              # print("{name} - {votes}".format(name=last_name, votes=candidate_votes))
      current_leader = max(leaders, key=leaders.get)
      results[state]['leader'] = current_leader
      for cand, vote_count in leaders.items():
        results[state][cand] = {'votes': vote_count}
        if cand == current_leader:
          next
        else:
          diff = leaders[current_leader] - vote_count
          results[state][cand]['diff'] = diff
          results[state]['tldr'] = '{current_leader} +{diff}'.format(current_leader=current_leader, diff=diff)
      total_votes_cast = sum(leaders.values())
      results[state]['totalVoteCounts'] = {}
      estimated_votes_low = estimated_votes["estimated_votes_low"]
      remaining_votes_low = estimated_votes_low - total_votes_cast
      
      estimated_votes_mid = estimated_votes["estimated_votes_mid"]
      remaining_votes_mid = estimated_votes_mid - total_votes_cast
      estimated_votes_high = estimated_votes["estimated_votes_high"]
      remaining_votes_high = estimated_votes_high - total_votes_cast
      results[state]['totalVoteCounts']['estimated_counts'] = [estimated_votes_low, estimated_votes_mid, estimated_votes_high]
      results[state]['totalVoteCounts']['remaining_votes'] = [remaining_votes_low, remaining_votes_mid, remaining_votes_high]
    print(json.dumps(results))

