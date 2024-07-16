import pandas as pd
import sys
sys.path.insert(0, '../')
#import identify_addresses as ia
from convert_to_compound import parse_event_csv
#from get_ens_name import get_ens_name


def get_min_quorum_members(events_df, proposalId):

    new_swayers = pd.DataFrame(columns=['voter', 'whale_count'])

    sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                    ['voter', 'votes']].sort_values(by='votes', ascending=False)

    sorted_by_votes.reset_index(inplace=True)

    majority = sorted_by_votes['votes'].sum() * 0.5
    cum_sum = 0


    for ind in sorted_by_votes.index:

        if cum_sum > majority:
            break

        cum_sum += sorted_by_votes['votes'][ind]
        new_swayer = pd.DataFrame(
            {'voter': [sorted_by_votes['voter'][ind]],
             'whale_count': [1]
             # 'name_from_comp_api': ia.get_compound_name(sorted_by_votes['voter'][ind])
             })
        new_swayers = pd.concat([new_swayers, new_swayer], ignore_index=True)


    return new_swayers

def make_mquorum_members_dfs_by_proposal(event_csvs):
    swayers = pd.DataFrame(columns=['voter', 'proposalId'])

    for csv_name in event_csvs:

        events_df = parse_event_csv(csv_name)

        for proposalId in events_df['proposalId'].dropna().unique():
            new_swayers = get_min_quorum_members(events_df, proposalId)
            new_swayers = pd.DataFrame( {'voter': new_swayers.voter, 'proposalId' : [proposalId]*new_swayers.shape[0] } )
            swayers = pd.concat( [swayers,new_swayers] )

    return swayers.sort_values(by='proposalId', ascending=True)



def make_mquorum_members_dfs(event_csvs):
    swayers = pd.DataFrame(columns=['voter', 'whale_count'])

    for csv_name in event_csvs:
        events_df = parse_event_csv(csv_name)

        for proposalId in events_df['proposalId'].dropna().unique():
            new_swayers = get_min_quorum_members(events_df, proposalId)

            for ind in new_swayers.index:
                if new_swayers['voter'][ind] in swayers['voter'].values:
                    swayers.loc[
                        swayers['voter'] == new_swayers['voter'][ind], 'whale_count'] = \
                        swayers.loc[
                            swayers['voter'] == new_swayers['voter'][ind], 'whale_count'] + 1
                else:
                    swayers = pd.concat([swayers, new_swayers.iloc[[ind]]], ignore_index=True)

    #nondatabase_ens_names = ia.make_ens_names_df()
    #sybil_names = ia.make_sybil_names_df()
    #swayers = swayers.merge(nondatabase_ens_names, on="voter", how="left").drop_duplicates()
    #swayers = swayers.merge(sybil_names, on='voter', how='left')
    #swayers['compound_api_name'] = swayers['voter'].apply(ia.get_compound_name)
    #swayers['ens_database_name'] = swayers['voter'].apply(get_ens_name)

    return swayers.sort_values(by='whale_count', ascending=False)


def get_actual_quorum_members(events_df, proposalId):
    new_swayers = pd.DataFrame(columns=['voter', 'whale_count'])
    supporters = pd.DataFrame(columns=['voter', 'whale_count'])
    opposers = pd.DataFrame(columns=['voter', 'whale_count'])

    sorted_by_votes = events_df.loc[events_df['proposalId'] == proposalId,
                                    ['voter', 'support', 'votes']].sort_values(
        by='votes', ascending=False)
    majority = sorted_by_votes['votes'].sum() * 0.5
    support_sum = oppose_sum = 0

    for ind in sorted_by_votes.index:

        if sorted_by_votes['support'][ind] == True:
            support_sum += sorted_by_votes['votes'][ind]
            supporters.loc[len(supporters.index)] = [sorted_by_votes['voter'][ind], 1]
        elif sorted_by_votes['support'][ind] == False:
            oppose_sum += sorted_by_votes['votes'][ind]
            opposers.loc[len(opposers.index)] = [sorted_by_votes['voter'][ind], 1]

        if support_sum > majority:
            new_swayers = pd.concat([new_swayers, supporters], ignore_index=True)
            break

        elif oppose_sum > majority:
            new_swayers = pd.concat([new_swayers, opposers], ignore_index=True)
            break

    return new_swayers


def make_aquorum_members_dfs(event_csvs):
    swayers = pd.DataFrame(columns=['voter', 'whale_count'])

    for csv_name in event_csvs:
        events_df = parse_event_csv(csv_name)

        for proposalId in events_df['proposalId'].dropna().unique():
            new_swayers = get_actual_quorum_members(events_df, proposalId)


            for ind in new_swayers.index:
                if new_swayers['voter'][ind] in swayers['voter'].values:
                    swayers.loc[
                        swayers['voter'] == new_swayers['voter'][ind], 'whale_count'] = \
                        swayers.loc[
                            swayers['voter'] == new_swayers['voter'][ind], 'whale_count'] + 1
                else:
                    swayers = pd.concat([swayers, new_swayers.iloc[[ind]]], ignore_index=True)

#    nondatabase_ens_names = ia.make_ens_names_df()
#    sybil_names = ia.make_sybil_names_df()
#    swayers = swayers.merge(nondatabase_ens_names, on="voter", how="left").drop_duplicates()
#    swayers = swayers.merge(sybil_names, on='voter', how='left')
#    swayers['compound_api_name'] = swayers['voter'].apply(ia.get_compound_name)
#    swayers['ens_database_name'] = swayers['voter'].apply(get_ens_name)

    return swayers.sort_values(by='whale_count', ascending=False)
