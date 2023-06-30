import json
import numpy as np
import pandas as pd
import math
import random


def spa(bid):
  winner = np.argmax(bid)
  price = np.partition(bid.flatten(), -2)[-2]
  return winner,price

#for i in range(n_step):
#  bid[i] = np.zeros(n_bidder)
#  reward[i] = np.zeros(n_bidder)
#  for j in range(n_bidder):
#    if budget[j] > 0:
#      bid[i][j] = np.random.uniform(0,budget[j])
#  winner,price=spa(bid[i])
#  reward[i][winner] = bid[i][winner] - price
#  budget[winner] -= price

n_bidder = 100
n_step = 1000
#budget = np.random.uniform(50,100,n_bidder)
bid = {}
reward = {}

d = {}
d['weekday'] = []
d['hour'] = []
d['auction_type'] = []
d['slotprice'] = []
d['payprice'] = []
d['click_prob'] = []
d['vid_len'] = []
n_day = 10
n_timestep = 96
n_bidding = 10

#  read dataset
pfivesres = json.load(open("/export/home/ziqin001/xpool/xpool/res4bid.json","r"))
onesres = json.load(open("/export/home/ziqin001/xpool/xpool/res4bid_1s.json","r"))
twosres = json.load(open("/export/home/ziqin001/xpool/xpool/res4bid_2s.json","r"))

all_vid = {}
vid_key = 0
#for key in 0p5sres:
#  all_vid[vid_key] = 0p5sres[key]
#  all_vid[vid_key]['vid_len'] = 0.5
#  vid_key += 1
#
#for key in 1p0sres:
#  all_vid[vid_key] = 1p0sres[key]
#  all_vid[vid_key]['vid_len'] = 1.0
#  vid_key += 1
#
#for key in 2p0sres:
#  all_vid[vid_key] = 2p0sres[key]
#  all_vid[vid_key]['vid_len'] = 2.0
#  vid_key += 1
#
#num_vid = len(all_vid)
print("start")
for i in range(n_day*n_timestep*n_bidding):

    offer_vidlen = random.choice([0.5,1.0,2.0])
    if i%(n_timestep*n_bidding)==0:
        #print("renew budget at step",i)
        budget = np.random.uniform(1,2,n_bidder)*1000000
    bid[i] = np.zeros(n_bidder)
    reward[i] = np.zeros(n_bidder)
    for j in range(n_bidder):
      if budget[j] > 0:
        #bid[i][j] = min(np.random.uniform(1,2),budget[j])
        bid[i][j] = min(offer_vidlen*np.random.uniform(0.92,1.08),budget[j])
    winner,price=spa(bid[i])
    reward[i][winner] = bid[i][winner] - price
    budget[winner] -= price
    if offer_vidlen == 0.5:
      winner_req = pfivesres[str(random.randint(0,len(pfivesres)-1))]
    elif offer_vidlen == 1.0:
      winner_req = onesres[str(random.randint(0,len(onesres)-1))]
    else:
      winner_req = twosres[str(random.randint(0,len(twosres)-1))]
    
    d['weekday'].append(math.floor(i/(n_timestep*n_bidding)))
    d['hour'].append(math.floor(i%(n_timestep*n_bidding)/n_bidding))
    d['auction_type'].append("SECOND_PRICE")
    #d[bidprice]
    d['slotprice'].append(0)
    d['payprice'].append(price)
    d['click_prob'].append(winner_req['sim'])
    d['vid_len'].append(offer_vidlen)
#    for j in range(n_timestep):
#        for k in range(n_bidding):

#print(d['weekday'].count(0),d['weekday'].count(9))
#print(d['hour'])

df = pd.DataFrame(data=d)
outfile = "data/ipinyou/data_1000.txt"
#outfile = "test.txt"
df.to_csv(outfile,sep="\t")




