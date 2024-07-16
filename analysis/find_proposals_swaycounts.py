import pandas as pd
import numpy as np
from datetime import datetime
from convert_to_compound import parse_event_csv


def find_min(events_df, proposalId):
    # skip invalid Uniswap proposal
    #     if ('uniswap_governor_alphav2' in x) & (i == 4):
    #         continue

    if 'timestamp' in events_df.columns:
        sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                        ['votes', 'timestamp']].sort_values(by='votes', ascending=False)
    else:
        sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                        ['votes']].sort_values(by='votes', ascending=False)

    majority = sorted_by_votes['votes'].sum() * 0.5
    cum_sum = 0
    min_voters = 0

    for ind in sorted_by_votes.index:

        if cum_sum > majority:
            break
        cum_sum += sorted_by_votes['votes'][ind]
        min_voters += 1

    if 'description' in events_df.columns:
        description = events_df.loc[
            (events_df['id'] == proposalId) & (events_df['event_name'] == 'ProposalCreated'), 'description']
        if not description.empty:
            description = description.values[0]
        else:
            description = np.nan
    else:
        description = np.nan

    proposal_events = events_df.loc[events_df['id'] == proposalId, 'event_name']
    if not proposal_events.empty:
        latest_event_name = proposal_events.iloc[-1]
    else:
        latest_event_name = np.nan

    new_proposal = pd.DataFrame(
        {'proposalId': proposalId, 'latest_event_name': latest_event_name,
         'min_voters': [min_voters], 'total_voters': [len(sorted_by_votes.index)],
         'voting_weight_threshold': [majority],
         'total_votes': [sorted_by_votes['votes'].sum()],
         'avg_weight_min_voters': round(cum_sum / min_voters / sorted_by_votes['votes'].sum(), 2),
         'description': description})
    if 'timestamp' in events_df.columns:
        new_proposal['timestamp'] = sorted_by_votes['timestamp'][ind]


    return new_proposal


def build_swaycounts_min(event_csvs):
    swaycounts_min = pd.DataFrame(
        columns=['proposalId', 'latest_event_name', 'timestamp', 'min_voters', 'total_voters',
                 'voting_weight_threshold', 'total_votes', 'avg_weight_min_voters', 'description'])

    for x in event_csvs:

        df = parse_event_csv(x)

        for proposalId in df['proposalId'].dropna().unique():
            new_proposal = find_min(df, proposalId)
            swaycounts_min = pd.concat([swaycounts_min, new_proposal], ignore_index=True)

    return swaycounts_min


def find_actual(events_df, proposalId, csv_name):

    if 'timestamp' in events_df.columns:
        sorted_by_votes = events_df.loc[
            events_df['proposalId'] == proposalId, ['support', 'votes', 'timestamp']
        ].sort_values(by='votes', ascending=False)
    else:
        sorted_by_votes = events_df.loc[
            events_df['proposalId'] == proposalId, ['support', 'votes']
        ].sort_values(by='votes', ascending=False)

    majority = sorted_by_votes['votes'].sum() * 0.5
    cum_sum = support_sum = oppose_sum = winning_sum = 0
    actual_min = min_voters = support_voters = oppose_voters = 0
    winning_side = ''
    quorum_met = False

    for ind in sorted_by_votes.index:

        if sorted_by_votes['support'][ind] == True:
            support_sum += sorted_by_votes['votes'][ind]
            support_voters += 1
        elif sorted_by_votes['support'][ind] == False:
            oppose_sum += sorted_by_votes['votes'][ind]
            oppose_voters += 1
        if cum_sum < majority:
            cum_sum += sorted_by_votes['votes'][ind]
            min_voters += 1
        if support_sum > majority:
            winning_side = 'support'
            actual_min = support_voters
            winning_sum = sorted_by_votes[sorted_by_votes['support'] == True]['votes'].sum()
            break
        elif oppose_sum > majority:
            winning_side = 'oppose'
            actual_min = oppose_voters
            winning_sum = sorted_by_votes[sorted_by_votes['support'] == False]['votes'].sum()
            break

    proposal_events = events_df.loc[events_df['id'] == proposalId, 'event_name']
    if not proposal_events.empty:
        latest_event_name = proposal_events.iloc[-1]
    else:
        latest_event_name = np.nan

    if 'compound' in csv_name:
        if winning_sum >= 400000:
            quorum_met = True
    elif 'uniswap' in csv_name:
        if winning_sum >= 40000000:
            quorum_met = True
    elif 'lido' in csv_name:
        if winning_sum >= 50000000:
            quorum_met = True


    new_proposal = pd.DataFrame(
        {'proposalId': proposalId, 'latest_event_name': latest_event_name, 'winning_side': winning_side,
         'winning_side_total_votes': winning_sum, 'quorum_met': quorum_met,
         'actual_to_sway': actual_min, 'total_voters': [len(sorted_by_votes.index)],
         'min_to_sway': min_voters})

    if 'timestamp' in events_df.columns:
        new_proposal['timestamp'] = sorted_by_votes['timestamp'][ind]

    new_proposal = new_proposal.astype({'proposalId': int, 'latest_event_name': str, 'winning_side' :str, 'winning_side_total_votes': float, 'quorum_met': bool, 'actual_to_sway': float, 'total_voters': int, 'min_to_sway': int })
        
    return new_proposal


def build_swaycounts_actual(event_csvs):
    swaycounts_actual_byweight = pd.DataFrame(
        columns=['proposalId', 'latest_event_name','winning_side',
                 'winning_side_total_votes', 'quorum_met','actual_to_sway',
                 'total_voters', 'min_to_sway', 'timestamp'])

    swaycounts_actual_byweight = swaycounts_actual_byweight.astype({'proposalId': int, 'latest_event_name': str, 'winning_side': str, 'winning_side_total_votes': float, 'quorum_met':bool, 'actual_to_sway': float, 'total_voters': int, 'min_to_sway': int})
    for csv_name in event_csvs:
        df = parse_event_csv(csv_name)

        for proposalId in df['proposalId'].dropna().unique():
            new_proposal = find_actual(df, proposalId, csv_name)
            swaycounts_actual_byweight = pd.concat([swaycounts_actual_byweight, new_proposal], ignore_index=True)
    return swaycounts_actual_byweight


def find_usd_sway(events_df, proposalId):

    if 'timestamp' in events_df.columns:
        sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                        ['votes', 'voter', 'usd_price', 'timestamp']].sort_values(by='votes', ascending=False)
    else:
        sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                        ['votes', 'voter', 'usd_price']].sort_values(by='votes', ascending=False)


    majority = sorted_by_votes['votes'].sum() * 0.5
    cum_votes = cum_usd_price = 0
    min_voters = 0

    for ind in sorted_by_votes.index:

        if cum_votes > majority:
            break
        cum_votes += sorted_by_votes['votes'][ind]
        # calculate USD price of votes at the time of the vote
        cum_usd_price += sorted_by_votes['votes'][ind] * sorted_by_votes['usd_price'][ind]
        min_voters += 1

    proposal_events = events_df.loc[events_df['id'] == proposalId, 'event_name']
    if not proposal_events.empty:
        latest_event_name = proposal_events.iloc[-1]
    else:
        latest_event_name = np.nan

    new_proposal = pd.DataFrame(
            {'proposalId': proposalId, 'latest_event_name': latest_event_name,
             'usd_amount_to_sway': [cum_usd_price], 'min_voters': min_voters,
             'min_voters_voting_weight': cum_votes, 'avg_usd_of_swayers': (cum_usd_price / min_voters)})

    if 'timestamp' in events_df:
        new_proposal['timestamp'] = sorted_by_votes['timestamp'][ind]

    return new_proposal


def build_usd_sway_dfs(event_csvs, usd_bytime):
    proposals_usd = pd.DataFrame(
        columns=['proposalId', 'latest_event_name',
                 'timestamp', 'usd_amount_to_sway',
                 'min_voters','min_voters_voting_weight',
                 'avg_usd_of_swayers'])

    for x in event_csvs:
        df = parse_event_csv(x)

        if 'timestamp' in df.columns:
            df['timestamp'] = (df['timestamp'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
            df['timestamp'] = df['timestamp'] * 1000
            df = df.sort_values(by='timestamp')

        if 'compound' in x:
            df = df[df['timestamp'] >= 1592280000000]

        df = pd.merge_asof(df, usd_bytime.sort_values(by='timestamp'), on="timestamp", direction="nearest")

        for proposalId in df['proposalId'].dropna().unique():
            new_proposal = find_usd_sway(df, proposalId)
            proposals_usd = pd.concat([proposals_usd, new_proposal], ignore_index=True)

    return proposals_usd
