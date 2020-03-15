#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        SensorPatt.py
#
# Purpose:     This module is used to create a tcp communication server to receive 
#              the Arduino_ESP8266 height data and do the PATT attestation. 
#              
# Author:       Yuancheng Liu
#
# Created:     2019/10/04
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import time
import random
import socket
import threading

from datetime import datetime
import globalVal as gv



#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class SensorPatt(object):
    """ TCP server thread.""" 
    def __init__(self, parent):
        self.terminate = False
        self.attitude = None            # sensor reading.
        self.checkSumfh = None          # filehandler to record the checksum.
        self.iterTime = -1              # Patt iteration time.
        self.blockNum = 4               # memory block size.
        self.stated = 'safe'          # Patt attestation result.
        # Init TCP communication channel:
        self.getCheckSum(self.blockNum)

        #-----------------------------------------------------------------------------
    def getCheckSum(self, number_of_blocks):
        """ Get the local firmware checkSum and the sensor feed back checkSum."""
        # Get the random memory address.
        s_b_and_s_w = self._generate_sb_and_sw()
        rhos = self._generate_random_block_select_list(
            s_b_and_s_w[0], s_b_and_s_w[1], number_of_blocks)
        address_list = self._generate_all_address(
            s_b_and_s_w[1], rhos, number_of_blocks)
        # Get the firmware from the local pre-saved firmware.
        verifier_checksum = self._calculate_sigma_star(address_list)
        print("telloSensor : verifier check sum %s" %
              str(verifier_checksum))
        # Connect to the sensor to get the firmware check sum.
        sensor_checksum = self._calculate_sigma_star(address_list)
        print("telloSensor : sensor check sum %s" %
              str(verifier_checksum))

        #self.checkSumfh.write(str(verifier_checksum)+"\n")
        #self.checkSumfh.write(str(sensor_checksum) + "\n")
        if str(verifier_checksum) != str(sensor_checksum):
            print("The check sum are different.")
            self.stated = 'unsafe'
            self.iterTime = 0 # stop iteration if the attesation find unsafe.
        else:
            print("The check sum are same.")
            self.stated = 'safe'
            self.iterTime -= 1 # decrease the iteration time for the next around.

#-----------------------------------------------------------------------------
    def _calculate_sigma_star(self, address_list):
        """ Load the local firmware sample and calculate the PATT check sum."""
        sigma_star = ""
        with open(gv.FIRM_FILE, "rb") as fh:
            bytesData = fh.read()
            for address in address_list:
                sigma_star = sigma_star + bytesData[address:address+1].hex()
        return str(sigma_star).upper()

#-----------------------------------------------------------------------------
    def _generate_sb_and_sw(self):
        """ Cenerate sb and sw LYC: (what are sb and sw stand for?)"""
        random.seed(datetime.now())
        return [random.randint(gv.RANDOM_RANGE_MIN, gv.RANDOM_RANGE_MAX) for i in range(2)]

#-----------------------------------------------------------------------------
    def _generate_random_block_select_list(self, s_b, s_w, number_of_blocks):
        """ Return a list of unduplicate number in [1, number_of_blocks]"""
        random.seed(s_b ^ s_w)
        return random.sample(range(1, number_of_blocks+1), number_of_blocks)

#-----------------------------------------------------------------------------
    def _generate_all_address(self, s_w, rhos, number_of_blocks):
        """ generate the randome memory address PATT need to check.
        """
        number_of_words = int(gv.FULL_MEMORY_SIZE_NODE_MCU // number_of_blocks)
        all_address_list = list()
        for rho in rhos:
            beta_list = self._generate_beta_list_for_block(
                s_w, rho, number_of_words)
            for line, beta in enumerate(beta_list):
                address = (gv.BOOT_LOADER_OFFSET + line + (rho-1)
                           * number_of_words) * gv.WORD_SIZE + beta
                all_address_list.append(address)
        return all_address_list

#-----------------------------------------------------------------------------
    def _generate_beta_list_for_block(self, s_w, rho, number_of_words):
        random.seed(rho ^ s_w)
        beta_list = [random.randint(0, gv.WORD_SIZE - 1) for _ in range(number_of_words)]
        return beta_list



def main():
    test = SensorPatt(None)


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()

