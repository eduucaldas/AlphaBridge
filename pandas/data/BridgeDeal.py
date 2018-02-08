#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:17:25 2018

@author: scander.mustapha
"""

class BridgeDeal:
    def __init__(self, bbo_file, hands, bidding, leader, dealer, lead, vuln):
        self.bbo_file = bbo_file
        self.tournament = None
        self.players = None
        self.hands = hands
        self.bidding = bidding
        self.leader = leader
        self.dealer = dealer
        self.lead = lead
        self.vuln = vuln
        
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
    
    def __str__(self):
        return "bbo_file={0},bidding={2},leader={3},dealer={4},lead={5},vuln={6}\
               ".format(self.bbo_file, self.lead, self.bidding, self.leader,\
                        self.dealer, self.lead, self.vuln)