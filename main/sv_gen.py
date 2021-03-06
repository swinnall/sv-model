" Evolutionary Model of Structural Variation ~ SVGen; Author: SamaxDSBel Winnall "

################################# comments ###################################



################################# imports ####################################

import numpy as np
import pandas as pd
import random
import csv
import sys

################################# classes ####################################

## Connections class
class ConnectionsClass():
    chrom = 0
    side  = 0
    id_   = 0
    haplo = 0
    cnid  = 0
    cn    = 0

    def __init__(self, chrom, side, id_, haplo, cnid, cn):
        self.chrom
        self.side
        self.id_
        self.haplo
        self.cnid
        self.cn

connection = ConnectionsClass(0,0,0,0,0,0)

################################################################################
## Writing SV data to file for Circos

class cirosPlot():
    chr1     = 0
    coord1   = 0
    strand1  = '+'
    chr2     = 0
    coord2   = 0
    strand2  = '+'
    extra    = 0
    hap      = 0
    cycleNum = 0
    SVtype   = 0

    def __init__(self, chr1, coord1, strand1, chr2, coord2, strand2, extra, hap, cycleNum, SVtype):
        self.chr1
        self.coord1
        self.strand1
        self.chr2
        self.coord2
        self.strand2
        self.extra
        self.hap
        self.cycleNum
        self.SVtype

    def insertions(self, nodes, cycleID, write_cicos = False, write_shatterseek = False):
        coveredNodes = []
        # for storing haplotype information for 22 chromosomes
        nIns = [ [0,0] for i in range(22)]

        # iterates along junctions in nodes list
        for i in range(len(nodes)):
            nodeID = nodes[i].get("nodeID")
            # appends to covered nodes to prevent recalling
            coveredNodes.append(nodeID)

            # checks segment is not deleted, has mutant connection, connects to non reference junction and is in daughter cell 1
            if nodes[nodeID].get("cn") > 0 and nodes[nodeID].get("M") != 'none' and \
                nodes[nodeID].get("position") != nodes[ int(nodes[nodeID].get("M")) ].get("position") and \
                nodes[nodeID].get("cellID") == 1:

                # checks node has an M connection
                if nodes[nodeID].get("M") != 'none':
                    connID = nodes[nodeID].get("M")

                    # checks it hasn't already been listed
                    if connID not in coveredNodes:

                        chr1     = nodes[nodeID].get("chromID")
                        coord1   = nodes[nodeID].get("position")
                        strand1  = '+'
                        chr2     = nodes[ int(nodes[nodeID].get("M")) ].get("chromID")
                        coord2   = nodes[ int(nodes[nodeID].get("M")) ].get("position")+1
                        strand2  = '+'
                        extra    = 'svtype=INS'
                        cycleNum = cycleID
                        SVtype   = 'TRA' # 'INS'

                        happ = nodes[nodeID].get("haplotype")
                        nIns[chr1-1][happ] += 1

                        # write to csv
                        if write_cicos:
                            with open('../output/circos/sv_data.tsv', 'a', newline='') as file:
                                writer = csv.writer(file, delimiter = '\t')
                                writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2,	extra, cycleNum])

                        # write to tsv - for ShatterSeek
                        if cycleNum == 1 and write_shatterseek:
                            with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                                writer = csv.writer(file, delimiter = '\t')
                                writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2, SVtype])

        return nIns

    def inversions(self, nodes, cycleID, chromLengths, write_cicos = False, write_shatterseek = False):
        coveredNodes = []
        nInv = [ [0,0] for i in range(22)]

        for i in range(len(nodes)):
            nodeID = nodes[i].get("nodeID")
            coveredNodes.append(nodeID)

            if nodes[nodeID].get("cn") > 0 and nodes[nodeID].get("inv") == True and \
                nodes[nodeID].get("cellID") == 1:

                # three types of segments so three statements, non Telomeric, p Telomeric and q Telomeric
                if nodes[nodeID].get("type") == 'nonTel':
                    adjID = nodes[ int(nodes[nodeID].get("WT")) ].get("nodeID")

                    if adjID not in coveredNodes:

                        chr1     = nodes[nodeID].get("chromID")
                        coord1   = nodes[nodeID].get("position")
                        strand1  = '+'
                        chr2     = chr1
                        coord2   = nodes[ int(nodes[nodeID].get("WT")) ].get("position")
                        strand2  = '+'
                        extra    = 'svtype=INV'
                        cycleNum = cycleID
                        SVtype   = 'h2hINV'

                        # populate counting inversions variable
                        happ = nodes[nodeID].get("haplotype")
                        nInv[chr1-1][happ] += 1

                        # write to csv
                        if write_cicos:
                            with open('../output/circos/sv_data.tsv', 'a', newline='') as file:
                                writer = csv.writer(file, delimiter = '\t')
                                writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2,	extra, cycleNum])

                        # write to tsv - for ShatterSeek
                        if cycleNum == 1 and write_shatterseek:
                            with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                                writer = csv.writer(file, delimiter = '\t')
                                writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2, SVtype])

                elif nodes[i].get("type") == 'pTel':

                    chr1     = nodes[nodeID].get("chromID")
                    coord1   = nodes[nodeID].get("position")
                    strand1  = '+'
                    chr2     = chr1
                    coord2   = 0
                    strand2  = '+'
                    extra    = 'svtype=INV'
                    cycleNum  = cycleID
                    SVtype   = 'h2hINV'

                    happ = nodes[nodeID].get("haplotype")
                    nInv[chr1-1][happ] += 1

                    # write to csv
                    if write_cicos:
                        with open('../output/circos/sv_data.tsv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter = '\t')
                            writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2,	extra, cycleNum])

                    # write to tsv - for ShatterSeek
                    if cycleNum == 1 and write_shatterseek:
                        with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter = '\t')
                            writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2, SVtype])

                elif nodes[i].get("type") == 'qTel':

                    chr1     = nodes[nodeID].get("chromID")
                    coord1   = nodes[nodeID].get("position")
                    strand1  = '+'
                    chr2     = chr1
                    coord2   = chromLengths[1][chr1-1]
                    strand2  = '+'
                    extra    = 'svtype=INV'
                    cycleNum  = cycleID
                    SVtype   = 'h2hINV'

                    happ = nodes[nodeID].get("haplotype")
                    nInv[chr1-1][happ] += 1

                    # write to csv
                    if write_cicos:
                        with open('../output/circos/sv_data.tsv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter = '\t')
                            writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2,	extra, cycleNum])

                    # write to tsv - for ShatterSeek
                    if cycleNum == 1 and write_shatterseek:
                        with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                            writer = csv.writer(file, delimiter = '\t')
                            writer.writerow([chr1, coord1, strand1, chr2, coord2, strand2, SVtype])

        return nInv

    def duplications(self, nodes, cycleID, nChroms, chromLengths, cn_df, num, size, write_cicos = False, write_shatterseek = False):
        # this Method populates the copy number dataframe (cn_df) with the CN information from the junctions
        # cn_df is initialised in cnProfiles function and provides the correct information format for plotting in Circos
        # for use in ShatterSeek the segments within cn_df are merged based on cn_valu, this is done in the SumStats function

        # code for populating cn_df based on nodes
        coveredNodes = []
        for i in range(len(nodes)):
            nodeID = nodes[i].get("nodeID")
            coveredNodes.append(nodeID)

            if nodes[nodeID].get("type") == 'pTel':
                chr1     = nodes[nodeID].get("chromID")
                start    = 0
                end      = nodes[nodeID].get("position")
                cn       = nodes[nodeID].get("cn")
                hap      = nodes[nodeID].get("haplotype")

                # converts hapltype into biological terminology
                if hap == 0:
                    hap = 'A'
                elif hap == 1:
                    hap = 'B'

                # finds segment index within cn data frame
                initPosIdx  = 0
                finalPosIdx = int( (end - start) / size )

                if finalPosIdx >= len(cn_df[chr1-1].get(hap)):
                    finalPosIdx = len(cn_df[chr1-1].get(hap))-1

                # iterates along cn_df and populates that segment's cn
                for segment in range( initPosIdx, finalPosIdx, 1 ):
                    cn_df[chr1-1].get(hap)[segment][2] = cn


            elif nodes[nodeID].get("type") == 'nonTel' and nodes[i].get("M") != 'none':
                adjID = int(nodes[nodeID].get("WT"))

                if adjID not in coveredNodes:
                    chr1     = nodes[nodeID].get("chromID")
                    start    = nodes[nodeID].get("position")
                    end      = nodes[adjID].get("position")
                    cn       = nodes[nodeID].get("cn")
                    hap      = nodes[nodeID].get("haplotype")

                    if hap == 0:
                        hap = 'A'
                    elif hap == 1:
                        hap = 'B'

                    initPosIdx  = int( start / size )
                    finalPosIdx = int( (end - start) / size )

                    if finalPosIdx >= len(cn_df[chr1-1].get(hap)):
                        finalPosIdx = len(cn_df[chr1-1].get(hap))-1

                    for segment in range( initPosIdx, finalPosIdx, 1 ):
                        cn_df[chr1-1].get(hap)[segment][2] = cn


            elif nodes[nodeID].get("type") == 'qTel':
                chr1     = nodes[nodeID].get("chromID")
                start    = nodes[nodeID].get("position")
                end      = chromLengths[1][chr1-1]
                cn       = nodes[nodeID].get("cn")
                hap      = nodes[nodeID].get("haplotype")

                if hap == 0:
                    hap = 'A'
                elif hap == 1:
                    hap = 'B'

                initPosIdx  = int( start / size )
                finalPosIdx = int( (end - start) / size )

                if finalPosIdx >= len(cn_df[chr1-1].get(hap)):
                    finalPosIdx = len(cn_df[chr1-1].get(hap))-1

                for segment in range( initPosIdx, finalPosIdx, 1 ):
                    cn_df[chr1-1].get(hap)[segment][2] = cn

        # code for printing out cn_df to tsv file
        for i in range(nChroms):
            for j in range(num[i]):

                chr1     = i+1
                start    = cn_df[i].get('A')[j][0]
                end      = cn_df[i].get('A')[j][1]

                cnA      = cn_df[i].get('A')[j][2]
                cnB      = cn_df[i].get('B')[j][2]
                cn_hap   = "cn={'%s': {'A': %s, 'B': %s}}" %(cnA+cnB,cnA,cnB)
                cycleNum = cycleID

                # write cn data - for circos
                if write_cicos:
                    with open('../output/circos/cn_data.tsv', 'a', newline='') as file:
                        writer = csv.writer(file, delimiter = '\t')
                        writer.writerow([chr1, start, end, cn_hap, cycleNum])

        return cn_df, num

calcSVs = cirosPlot(0,0,'+',0,0,'+',0,0,0,0)


################################################################################
## 'Check' Methods

class CheckBool():
    def __init__(self):
        return

    def endGrowth(nodes, lmbda, verbose = 0):
        # checks how many remaining breaks there are in G1
        # if less than lambda then G1 will stop
        tally = 0
        for i in range(len(nodes)):

            if nodes[i].get("M") == 'none' and nodes[i].get("cn") > 0:
                tally += 1
        if verbose > 0:
            print("%d remaining junctions.\n" %tally)

        if tally <= lmbda:
            endCondition = False
            if verbose > 0:
                print("End of growth function.\n")
        else:
            endCondition = True

        return endCondition

    def TelCheck(nodes,nodeID):
        # this method checks whether a node is telomeric
        # method is used in while loop conditions
        telCondition = True

        if nodes[nodeID].get("type") == 'qTel' or nodes[nodeID].get("type") == 'pTel':
            telCondition = False

        else:
            telCondition = True

        return telCondition

    def checkCentromere(nodes,pathList,i, verbose=0):
        # counts how many centromeres there are in a defined path
        tally    = 0
        centList = []
        if verbose > 0:
            print('\nnext centromere list info: ')
        for j in range(len(pathList.get(str(i)))):
            nodeID = pathList.get(str(i))[j]

            # Tel types have one junction referring to a centromere
            if nodes[nodeID].get("centromeric") == True and nodes[nodeID].get("type") != 'nonTel':
                tally += 1
                centList.append(nodeID)

            # nonTel types have two junctions referring to the same centromere
            elif nodes[nodeID].get("centromeric") == True and nodes[nodeID].get("type") == 'nonTel':
                tally += 0.5
                centList.append(nodeID)

        nCent = tally
        return nCent, centList

################################################################################
## Function initialising cn segments for discretizing simulation data
def cnProfiles(nChroms, chromLengths, size):

    # create data frame
    cn_df = [{} for i in range(nChroms)]

    # initialise number of segments per chromosome
    num = [0 for i in range(nChroms)]

    # initialise data frame
    for i in range(nChroms):

        # number of segments per chromosomes
        num[i] = int(chromLengths[1][i] / size)

        # construct lists for appending
        cn_df[i]['A'] = []
        cn_df[i]['B'] = []

        for j in range(num[i]):

            # append segment info of "start, end, cn"
            cn_df[i]['A'].append( [j*size, j*size + size, 1] )
            cn_df[i]['B'].append( [j*size, j*size + size, 1] )

    return cn_df, num, size


################################################################################
## Functions for biology

def generateDSBs(minDSB, maxDSB):
    # introduces DSBs into the genome prior to G1 repair
    nDSB = int(random.randint(minDSB,maxDSB))

    return nDSB


def matPref(matType, nChroms):
    # chromMat is a probability matrix for selecting chromosomes

    if matType == 'random':
        # equal probability of selecting each chromosome
        chromMat = [ 1/nChroms for i in range(nChroms)]
        nBiasedChroms = 0

    elif matType == 'biased':
        chromMat = [0 for i in range(nChroms)]
        # randomly select number of chromosomes to choose from
        nBiasedChroms = random.randint(1,3)
        # choose the chromosomes
        selectedChromosomes = np.random.choice([i for i in range(nChroms)], nBiasedChroms, replace = False)

        # assign probabilities; bias towards the selected chromosomes
        p0 = 0.667
        p1 = p0/nBiasedChroms
        p2 = (1-p0)/(nChroms-nBiasedChroms)

        for i in range(nChroms):
            if i in selectedChromosomes:
                chromMat[i] = p1
            else:
                chromMat[i] = p2

    elif matType == 'fixed':
        chromMat = [0 for i in range(nChroms)]
        # same probability bias as before for reproducibility
        # choose g target chromosomes, -1 for index, advised to choose up to 3 targets max
        g1 = 3
        # g2 = 5
        selectedChromosomes = [g1-1]
        # selectedChromosomes = [g1-1, g2-1] # exmaple of 3 targets: [g1-1, g2-1, g3-1]
        nBiasedChroms = len(selectedChromosomes)

        p0 = 0.667
        p1 = p0/nBiasedChroms
        p2 = (1-p0)/(nChroms-nBiasedChroms)

        for i in range(nChroms):
            if i in selectedChromosomes:
                chromMat[i] = p1
            else:
                chromMat[i] = p2

    return chromMat, nBiasedChroms


def generateNodes(nodes,nDSB,nChroms,chromLengths,firstEvent,chromMat,DSBmat, verbose = 0):
    if verbose > 0:
        print("\nEntering node generation\n")

    # reset prev path information
    for i in range(len(nodes)):
        if  nodes[i].get("cn") > 0:
            nodes[i]["type"]        = 'nonTel'
            nodes[i]["WT"]          = 'none'
            nodes[i]["centromeric"] = False
            nodes[i]["inv"]         = False

    # determine nbp on each chromosome prior to additional assignment; if 0 then cn = 1; else: call check func later
    # stores number of break points per chrom (row) for each haplotype (column)
    nbp_per_chrom = [ [0,0] for i in range(nChroms)]
    for i in range(len(nodes)):
        hapIndex = nodes[i].get("haplotype")
        chrIndex = nodes[i].get("chromID")-1 # -1 for index

        nbp_per_chrom[chrIndex][hapIndex] = nbp_per_chrom[chrIndex][hapIndex] + 1

    # local definitions
    uniqueID = len(nodes)
    hapChoice = [0,1]

    # nThreshold is the marker between nNodes in each cell cycle
    nThreshold = len(nodes)

    # twice the number of breakpoints added (each break point has a left and right junction)
    for i in range(0, 2*nDSB, 2):

        ## generate positional information
        # chooses chromosome based on chromMat probability distribution
        chromosomeTarget = int( np.random.choice([i for i in range(nChroms)], 1, p = chromMat) ) + 1 # +1 for index
        breakpointPos    = random.randint(0, chromLengths[1][chromosomeTarget-1])
        haplotype        = np.random.choice(hapChoice, 1)

        # update number of DSBs per chrom per haplotype
        DSBmat[chromosomeTarget-1][haplotype[0]] += 1

        # define information that defines a junction/node
        nodeData = {
            # identification:
            "nodeID":    uniqueID,
            "cellID":    1,
            "chromID":   chromosomeTarget,
            "haplotype": haplotype[0],
            "position":  breakpointPos,
            "side":      0,
            "cn":        'temp',
            "cnID":      'temp',
            # connections:
            "type":        'nonTel',
            "WT":          'none',
            "M":           'none',
            # properties:
            "centromeric": False,
            "inv":         False,
        }
        nodes.append(nodeData)
        uniqueID += 1

        nodeData = {
            # identification:
            "nodeID":    uniqueID,
            "cellID":    1,
            "chromID":   chromosomeTarget,
            "haplotype": haplotype[0],
            "position":  breakpointPos,
            "side":      1,
            "cn":        'temp',
            "cnID":      'temp',
            # connections:
            "type":        'nonTel',
            "WT":          'none',
            "M":           'none',
            # properties:
            "centromeric": False,
            "inv":         False,
        }
        nodes.append(nodeData)
        uniqueID += 1

    if verbose > 0:
        print("\nDetermining cn information\n")

    # initialise cn information
    if firstEvent == True:
        # first event is defined as the cell cycle where DSBs are FIRST introduced
        # cell cycle 1 could be introduce no DSBs and cell cycle 2 introduce 6: cell cycle 2 would be the first event

        if len(nodes) == 0:
            # check function - nodes should not be empty.
            if verbose > 0:
                print("nodes empty - Unintended.")
            sys.exit()

        # cn would be default values in this scenario
        for i in range(len(nodes)):
            nodes[i]["cnID"] = 1
            nodes[i]["cn"]   = 1

    # no change to system
    elif firstEvent == False and nDSB == 0:
        pass

    # non initial event
    elif firstEvent == False and nDSB > 0:

        # assumed no cn is greater than 5 in simulation (currently cn = 5 is an impossible scenario)
        cnidList   = [i for i in range(1,5)]

        # assign cn info for newly appended junctions
        for i in range(nThreshold, len(nodes), 2):

            # list of available cnIDs
            cnidChoice = []

            # if no breaks on a chromosome then it has cn = 1
            if nbp_per_chrom[nodes[i].get("chromID")-1][nodes[i].get("haplotype")] == 0:
                nodes[i]["cnID"]   = 1
                nodes[i]["cn"]     = 1
                nodes[i+1]["cnID"] = 1
                nodes[i+1]["cn"]   = 1

            # try different cnIDs, pick randomly between the ones that exist
            else:
                for j in cnidList:

                    # set index coords every cnID attempt
                    nodeID = i
                    nodes[nodeID]["cnID"]   = j
                    nodes[nodeID+1]["cnID"] = j

                    # those that exist will provide non np.pi return in >= 1 direction
                    for k in range(2):

                        adjID = findAdjacentJunction(nodes,nodeID)

                        if adjID == np.pi:
                            nodeID = i+1
                        else:
                            cnidChoice.append( (j, nodes[adjID].get("cn"), nodes[nodeID].get("side"), nodes[adjID].get("side")) )
                            break # prevents repeat assignment

                # choose cnID location based on which nodes define the segment (opposite directions/sides)
                for l in range(len(cnidChoice)):
                    idxChoice = cnidChoice[l]
                    if idxChoice[2] != idxChoice[3]:
                        cnRef = idxChoice
                        break

                # assign cnid
                nodes[i]["cnID"]   = cnRef[0]
                nodes[i+1]["cnID"] = cnRef[0]

                # assign cn
                nodes[i]["cn"]   = cnRef[1]
                nodes[i+1]["cn"] = cnRef[1]

    return nodes, DSBmat


def generateTelomeres(nodes, verbose = 0):
    # generates telomeres based on whether a junction has any adjacent junctions further along the chromosome
    # i.e. if there are none, adjID = np.pi
    if verbose > 0:
        print("\nEntering telomere generation\n")

    for i in range(len(nodes)):
        nodeID = nodes[i].get("nodeID")

        direction = nodes[nodeID].get("side")
        adjID = findAdjacentJunction(nodes,nodeID)

        if adjID == np.pi and direction == 1:
            nodes[nodeID]["type"] = 'qTel'

        elif adjID == np.pi and direction == 0:
            nodes[nodeID]["type"] = 'pTel'

        else: pass

    return nodes


def findAdjacentJunction(nodes,nodeID):
    rightAdjNodes = []
    leftAdjNodes  = []
    temp          = []

    direction = nodes[nodeID].get("side")
    location  = nodes[nodeID].get("position")

    connection.id_   = nodeID
    connection.chrom = nodes[nodeID].get("chromID")
    connection.cnid  = nodes[nodeID].get("cnID")
    connection.haplo = nodes[nodeID].get("haplotype")


    # locates junctions along the chromosome in LR direction
    for i in range(len(nodes)):
        if nodes[i].get("chromID") == connection.chrom                    \
            and nodes[i].get("cnID") == connection.cnid                   \
            and nodes[i].get("haplotype") == connection.haplo             \
            and direction == 1 and nodes[i].get("position") > location:
                rightAdjNodes.append(nodes[i])

        elif nodes[i].get("chromID") == connection.chrom                  \
            and nodes[i].get("cnID") == connection.cnid                   \
            and nodes[i].get("haplotype") == connection.haplo             \
            and direction == 0 and nodes[i].get("position") < location:
                leftAdjNodes.append(nodes[i])


    # Right Case: sorts list of potential junctions
    if len(rightAdjNodes) > 0:
        rightAdjNodes.sort(key = lambda x:x['position'])

        # only telomere available
        if len(rightAdjNodes) == 1:
            nodeID = rightAdjNodes[0].get("nodeID")

        # closest position chosen
        elif len(rightAdjNodes) > 1:
            for i in range(len(rightAdjNodes)):

            # right direction: next junction is the left side of a breakpoint
                if rightAdjNodes[i].get("side") == 0:
                    nodeID = rightAdjNodes[i].get("nodeID")
                    break # stops at first case


    # Left Case: sorts list of potential junctions
    elif len(leftAdjNodes) > 0:
        leftAdjNodes.sort(key = lambda x:x['position'], reverse = True)

        # only telomere available
        if len(leftAdjNodes) == 1:
            nodeID = leftAdjNodes[0].get("nodeID")

        # closest position chosen
        elif len(leftAdjNodes) > 1:
            for i in range(len(leftAdjNodes)):

            # right direction: next junction is right
                if leftAdjNodes[i].get("side") == 1:
                    nodeID = leftAdjNodes[i].get("nodeID")
                    break # stops at first case


    # no adjacent junctions means segment is telomeric, return pi
    elif len(leftAdjNodes) == 0 and len(rightAdjNodes) == 0:
        nodeID = np.pi

    return nodeID


def g1(nodes, lmbda, verbose = 0):
    if verbose > 0:
        print('\nEntering G1\n')

    # list available wild type connections
    # must not be deleted and must be a non-telomeric segment
    lWT = []
    for i in range(len(nodes)):
        if nodes[i].get("cn") > 0 and nodes[i].get("type") == 'nonTel':
            lWT.append(nodes[i].get("nodeID"))


    # check lWT has elements
    if len(lWT) > 0:
        WTcondition = True
    else: WTcondition = False

    if verbose > 0:
        print('Generating WT Connections')

    # generate WT connections
    while WTcondition:

        nodeID = int(np.random.choice(lWT, 1))
        adjID = findAdjacentJunction(nodes,nodeID)

        # checks not connecting to telomere or repeated junctions
        if adjID in lWT:

            # assign connections
            nodes[nodeID]["WT"] = str(adjID)
            nodes[adjID]["WT"]  = str(nodeID)

            if verbose > 1:
                print("start J:  %s" %nodeID)
                print("WT J:     %s\n" %adjID)

            # prevent repeat assignment
            lWT.remove(nodeID)
            lWT.remove(adjID)


        # check end condition
        if len(lWT) > 0:
            WTcondition = True
        else: WTcondition = False

    if verbose > 0:
        print('Generating M Connections\n')
    # list available mutant connections
    lM = []
    for i in range(len(nodes)):
        if nodes[i].get("cn") > 0 and nodes[i].get("M") == 'none' and nodes[i].get("cellID") == 1:
            lM.append(nodes[i].get("nodeID"))


    # repairs these breaks until endCondition is met, i.e. is number of 'unrepairs' < lambda
    endCondition = True
    while endCondition == True:

        # catch statement for low DSB cycles
        if len(lM) < 2:
            break

        ## start at random junction
        startNode = int(np.random.choice(lM, 1))

        # join random junction
        joinChoice = True
        while joinChoice:

            joinNode = int(np.random.choice(lM, 1))

            if joinNode != startNode:
                lM.remove(startNode)
                lM.remove(joinNode)
                joinChoice = False

        # assign connection
        nodes[startNode]["M"] = str(joinNode)
        nodes[joinNode]["M"]  = str(startNode)

        if verbose > 1:
            print("start J:  %s" %startNode)
            print("joined J: %s" %joinNode)

        endCondition = CheckBool.endGrowth(nodes, lmbda, verbose)

    return nodes


def generateCentromeres(nodes, centromerePos):

    # iterates along list of junctions, assigns centromeric = True property
    # based on junction position relating to true genomic centromere position

    for i in range(len(nodes)):
        nodeID = nodes[i].get("nodeID")

        # check non telomeric segments
        if nodes[nodeID].get("type") == 'nonTel' and nodes[nodeID].get("cn") > 0:
            connID = int(nodes[nodeID].get("WT"))
            chromosome = nodes[nodeID].get("chromID")-1 # for index

            # left direction
            if nodes[nodeID].get("side") == 0 and centromerePos[chromosome] < nodes[nodeID].get("position") \
                and centromerePos[chromosome] > nodes[connID].get("position"):

                    nodes[nodeID]["centromeric"] = True
                    nodes[connID]["centromeric"] = True

            # right direction
            elif nodes[nodeID].get("side") == 1 and centromerePos[chromosome] > nodes[nodeID].get("position") \
                and centromerePos[chromosome] < nodes[connID].get("position"):

                    nodes[nodeID]["centromeric"] = True
                    nodes[connID]["centromeric"] = True
            else: pass

        # check telomeric segments
        elif nodes[nodeID].get("type") != 'nonTel' and nodes[nodeID].get("cn") > 0:
            chromosome = nodes[nodeID].get("chromID")-1 # for index

            if nodes[nodeID].get("type") == 'pTel' \
                and centromerePos[chromosome] < nodes[nodeID].get("position"):

                    nodes[nodeID]["centromeric"] = True

            elif nodes[nodeID].get("type") == 'qTel' \
                and centromerePos[chromosome] > nodes[nodeID].get("position"):

                    nodes[nodeID]["centromeric"] = True
            else: pass

    return nodes


def connectedPathConstruction(nodes, pathList, verbose = 0):
    # defines paths that start and end on a telomere prior to S phase
    # i.e. these paths are fully connected upon completion of G1
    if verbose > 0:
        print("Entering Path Construction - Connected")

    # locates all p telomeric junctions and sets as start of path
    pTel = []
    for i in range(len(nodes)):
        nodeID = nodes[i].get("nodeID")
        if nodes[nodeID].get("type") == 'pTel' and nodes[nodeID].get("cn") > 0:
            pTel.append(nodeID)


    # iterates along each path, checking for adjacent connections
    for i in pTel:
        temp = []; nodeID = i
        temp.append(nodeID)

        # condition stops at another telomere
        telCondition = True
        while telCondition:

            # check next connection (maxDSBtant)
            if nodes[nodeID].get("M") != 'none':
                nodeID = int(nodes[nodeID].get("M"))
                temp.append(nodeID)

                # debugging
                #if nodes[nodeID].get("M") != 'none':
                #    print(nodes[int(nodes[nodeID].get("M"))])
                #if nodes[nodeID].get("WT") != 'none':
                #    print(nodes[int(nodes[nodeID].get("WT"))])

                # check next connection (Wild Type)
                if nodes[nodeID].get("WT") != 'none':
                    nodeID = int(nodes[nodeID].get("WT"))
                    temp.append(nodeID)

                # checks if segment is telomeric
                else:
                    telCondition = CheckBool.TelCheck(nodes,nodeID)

            # no mutant connection; path unconnected & irrelevant
            else:
                temp.clear()
                break


         # check for paths defined by two identical pTelomeres
        if len(temp) > 0:
            for i in range(len(pathList)):
                # if end junction == start junction of a previous path: clear to prevent repitition
                if temp[-1] in pathList.get(str(i)):
                    temp.clear()
                    break


        # append to end of pathList
        if len(temp) > 0:
            nPaths = len(pathList)
            pathList[str(nPaths)] = temp
            if verbose > 0:
                print("Connected path: %s\n" %temp)

    return pathList


def unconnectedPathConstruction(nodes, verbose = 0):
    # stores unconnected paths for parsing to S phase
    if verbose > 0:
        print("Entering Path Construction - Unconnected")

    unconnected  = []
    telomeric    = []
    nonTelomeric = []

    # locates all unconnected junctions
    for i in range(len(nodes)):
        nodeID = nodes[i].get("nodeID")
        if nodes[nodeID].get("M") == 'none' and nodes[nodeID].get("cn") > 0:
            unconnected.append(nodeID)
    if verbose > 0:
        print("Unconnected junctions: %s" %unconnected)


    # identifies replication type for the unconnected segments
    for i in range(len(unconnected)):
        temp   = []
        nodeID = unconnected[i]
        temp.append(nodeID)

        # follows paths starting from unconnected junctions
        endPathCondition = True
        while endPathCondition:

            # checks next connection (WT)
            if nodes[nodeID].get("WT") != 'none':
                nodeID = int(nodes[nodeID].get("WT"))
                temp.append(nodeID)

                # checks next connection (M)
                if nodes[nodeID].get("M") != 'none':
                    nodeID = int(nodes[nodeID].get("M"))
                    temp.append(nodeID)


                # if M == 'none': path ends on non-telomere
                else: break

            # if WT == 'none': path ends on telomere
            else:
                telCondition = CheckBool.TelCheck(nodes,nodeID)
                if telCondition == False:
                    break
                else:
                    print(nodes[nodeID])
                    sys.exit("Error in unconnected path construction")


        # unconnected path ends on telomere:
        if nodes[nodeID].get("type") == 'pTel' or nodes[nodeID].get("type") == 'qTel':
            telomeric.append(temp)

        # unconnected path ends on non-telomere:
        elif nodes[nodeID].get("type") == 'nonTel':

            # check for repeats
            for i in range(len(nonTelomeric)):
                if temp[-1] in nonTelomeric[i]:
                    temp = []
                    break

            if len(temp) > 0:
                nonTelomeric.append(temp)

    if verbose > 0:
        print("unconnected telomeric segments:     %s" %telomeric)
        print("unconnected non-telomeric segments: %s" %nonTelomeric)

    return telomeric, nonTelomeric


def syn_g2(nodes, pathList, telomeric, nonTelomeric, verbose = 0):
    # S phase going into G2
    # firstly replicates unconnected paths by adding new junctions (S)
    # then connects them (G2)
    if verbose > 0:
        print('\nEntering S, G2\n')

    # lists for copied junctions
    telomericCopied    = [[] for i in range(len(telomeric))]
    nonTelomericCopied = [[] for i in range(len(nonTelomeric))]

    # 1. unconnected telomeric paths
    uniqueID = len(nodes)
    for i in range(len(telomeric)):
        if verbose > 0:
            print("\nNew path, key i: %s" %i)

        # introduces new nodes to complete path
        for j in range(len(telomeric[i])):
            nodeID = telomeric[i][j]

            nodes[nodeID]["cn"] = nodes[nodeID].get("cn") + 1
            nodes.append({
                "nodeID":    uniqueID,
                "cellID":    nodes[nodeID].get("cellID"),
                "chromID":   nodes[nodeID].get("chromID"),
                "haplotype": nodes[nodeID].get("haplotype"),
                "position":  nodes[nodeID].get("position"),
                "side":      nodes[nodeID].get("side"),
                "cn":        nodes[nodeID].get("cn"),
                "cnID":      nodes[nodeID].get("cn"),

                "type":      nodes[nodeID].get("type"),
                "WT":        '',
                "M":         '',

                "centromeric": nodes[nodeID].get("centromeric"),
                "inv":         False,
            })
            telomericCopied[i].append(uniqueID)
            uniqueID += 1

        if verbose > 0:
            print("%d node(s) added (unconnected path length)" %len(telomeric[i]))

        # creates path
        temp = []
        for j in reversed(telomeric[i]):
            temp.append(j)

        for j in telomericCopied[i]:
            temp.append(j)

        # stores path information
        if len(temp) > 0:
            nPaths = len(pathList)
            pathList[str(nPaths)] = temp


        # path key:
        I = len(pathList)-1
        if verbose > 0:
            print("telomeric: %s" %telomeric[i])
            print("PathList:  %s" %pathList.get(str(I)))


        # connection information
        if len(pathList.get(str(I))) == 2:

            nodes[ pathList.get(str(I))[0] ]["M"]  = str( pathList.get(str(I))[1] )
            nodes[ pathList.get(str(I))[1] ]["M"]  = str( pathList.get(str(I))[0] )

            nodes[ pathList.get(str(I))[1] ]["WT"] = 'none'

        elif len(pathList.get(str(I))) > 2:

            for j in range(0, len(pathList.get(str(I)))-1, 2):

                if j == 0:
                    # starting junction is telomeric so only connect to adjacent junction in right direction of path
                    nodes[ pathList.get(str(I))[j]   ]["M"]  = str( pathList.get(str(I))[j+1] )
                    nodes[ pathList.get(str(I))[j+1] ]["M"]  = str( pathList.get(str(I))[j]   )

                else:
                    # bidirectional path connections
                    nodes[ pathList.get(str(I))[j]   ]["M"]  = str( pathList.get(str(I))[j+1] )
                    nodes[ pathList.get(str(I))[j+1] ]["M"]  = str( pathList.get(str(I))[j]   )

                    nodes[ pathList.get(str(I))[j]   ]["WT"]  = str( pathList.get(str(I))[j-1] )
                    nodes[ pathList.get(str(I))[j-1] ]["WT"]  = str( pathList.get(str(I))[j]   )

            nodes[ pathList.get(str(I))[ len(pathList.get(str(I)))-1 ] ]["WT"]  = 'none'


    # 2. unconnected non telomeric paths:
    uniqueID = len(nodes)
    for i in range(len(nonTelomeric)):

        # introduces new nodes to complete path
        for j in range(len(nonTelomeric[i])):
            nodeID = nonTelomeric[i][j]

            nodes[nodeID]["cn"] = nodes[nodeID].get("cn") + 1
            nodes.append({
                "nodeID":    uniqueID,
                "cellID":    nodes[nodeID].get("cellID"),
                "chromID":   nodes[nodeID].get("chromID"),
                "haplotype": nodes[nodeID].get("haplotype"),
                "position":  nodes[nodeID].get("position"),
                "side":      nodes[nodeID].get("side"),
                "cn":        nodes[nodeID].get("cn"),
                "cnID":      nodes[nodeID].get("cn"),

                "type":        nodes[nodeID].get("type"),
                "WT":          '',
                "M":           '',
                "centromeric": nodes[nodeID].get("centromeric"),
                "inv":         False,
            })
            nonTelomericCopied[i].append(uniqueID)
            uniqueID += 1

        # creates path
        temp = []
        for j in nonTelomeric[i]:
            temp.append(j)

        for j in reversed(nonTelomericCopied[i]):
            temp.append(j)


        if len(temp) > 0:
            nPaths = len(pathList)
            pathList[str(nPaths)] = temp
        else: pass

        I = len(pathList)-1
        if verbose > 0:
            print("non-telomeric: %s" %nonTelomeric[i])
            print("PathList:      %s" %pathList.get(str(I)))

        # connection information
        for j in range(0, len(pathList.get(str(I)))-1, 2):

            if j == 0:
                # completed path is circular
                # first junction must connect to the final junction in pathlist to complete path (i.e. travelling in left direction)
                nodes[ pathList.get(str(I))[j]   ]["M"]  = str( pathList.get(str(I))[-1] )
                nodes[ pathList.get(str(I))[-1]  ]["M"]  = str( pathList.get(str(I))[j]  )
                # in right direction, make connection to j+1 element of pathlist
                nodes[ pathList.get(str(I))[j]   ]["WT"]  = str( pathList.get(str(I))[j+1] )
                nodes[ pathList.get(str(I))[j+1] ]["WT"]  = str( pathList.get(str(I))[j]   )


            else:
                nodes[ pathList.get(str(I))[j]   ]["M"]  = str( pathList.get(str(I))[j-1] )
                nodes[ pathList.get(str(I))[j-1] ]["M"]  = str( pathList.get(str(I))[j]   )

                nodes[ pathList.get(str(I))[j]   ]["WT"]  = str( pathList.get(str(I))[j+1] )
                nodes[ pathList.get(str(I))[j+1] ]["WT"]  = str( pathList.get(str(I))[j]   )

    return nodes, pathList


def checkInv(nodes, pathList):
    # checks whether a segment (accessed via the junction) is inverted; as inferred via the list of paths
    # if segment is inverted, node property "inv" = True

    for i in range(len(pathList)):
        for j in range(len(pathList.get(str(i)))):
            nodeID = pathList.get(str(i))[j]

            if nodes[ int(nodes[nodeID].get("M")) ].get("side") == 0 and nodes[nodeID].get("cn") > 0:
                nodes[nodeID]["inv"] = True

    return nodes


def cmplxSegregation(nodes, pathList, i, nCent, centList, centromerePos, DSBmat, nMitosisBreaks, verbose = 0):
    # called when number of centromeres in a path exceeds 1
    # function chooses breakpoint location, introduces new breakpoints and forms connections

    # list of introduced junctions
    newJuncList = []

    # a threshold variable for iterating along PathList
    m = 0

    # a threshold variable for iterating along centList
    n = 0

    # nCent - 1 = number of breakpoints
    nMitosisBreaks += nCent - 1

    # iterate along for number of breaks
    for j in range(int(nCent)-1):

        # segment options for breakpoints
        options = []

        for k in range(m, len(pathList.get(str(i))), 1):
            nodeID = pathList.get(str(i))[k]

            # appends first centromeric node
            if nodeID == centList[n] and len(options) == 0:
                options.append(nodeID)

            # appends nodes between centromeres
            elif nodeID != centList[n+1] and len(options) != 0:
                options.append(nodeID)

            # appends second centromeric node, ending options
            elif nodeID == centList[n+1] and len(options) != 0:
                options.append(nodeID)
                # m becomes start point for next breakpoint
                m = k+1
                n = n+2
                break


        # choosing segment to insert breakpoint
        nodeChoice = int(np.random.choice(options,1))
        if verbose > 0:
            print("\noptions: %s" %options)
            print("decision: %s" %nodeChoice)


        # positional information
        jPos    = nodes[nodeChoice].get("position")
        jChrom  = nodes[nodeChoice].get("chromID")
        segType = nodes[nodeChoice].get("type")
        centPos = int(centromerePos[jChrom-1])


        # choosing breakpoint position given the segment type
        if segType == 'pTel':
            pos = random.randint(centPos, jPos)


        elif segType == 'qTel':
            pos = random.randint(jPos, centPos)


        elif segType == 'nonTel' and nodes[nodeChoice].get("centromeric") == True:

            if jPos > centPos:
                pos = random.randint(centPos, jPos)

            elif jPos < centPos:
                pos = random.randint(jPos, centPos)


        elif segType == 'nonTel' and nodes[nodeChoice].get("centromeric") == False:
            connID = int(nodes[nodeChoice].get("WT"))

            if jPos > nodes[connID].get("position"):
                pos = random.randint(nodes[connID].get("position"), jPos)

            elif jPos < nodes[connID].get("position"):
                pos = random.randint(jPos, nodes[connID].get("position"))


        # appending new breakpoints to nodes
        uniqueID = len(nodes)
        nodes.append({
            "nodeID":    uniqueID,
            "cellID":    nodes[nodeChoice].get("cellID"),
            "chromID":   jChrom,
            "haplotype": nodes[nodeChoice].get("haplotype"),
            "position":  pos,
            "side":      0,
            "cn":        nodes[nodeChoice].get("cn"),
            "cnID":      nodes[nodeChoice].get("cnID"),

            "type":        'nonTel',
            "WT":          'none',
            "M":           'none',
            "centromeric": False,
            "inv":         nodes[nodeChoice].get("inv"),
        })
        nodes.append({
            "nodeID":    uniqueID+1,
            "cellID":    nodes[nodeChoice].get("cellID"),
            "chromID":   jChrom,
            "haplotype": nodes[nodeChoice].get("haplotype"),
            "position":  pos,
            "side":      1,
            "cn":        nodes[nodeChoice].get("cn"),
            "cnID":      nodes[nodeChoice].get("cnID"),

            "type":        'nonTel',
            "WT":          'none',
            "M":           'none',
            "centromeric": False,
            "inv":         nodes[nodeChoice].get("inv"),
        })
        newJuncList.append(uniqueID)
        newJuncList.append(uniqueID+1)

        # update the number of double strand breaks per chrom per haplotype
        DSBmat[jChrom-1][nodes[nodeChoice].get("haplotype")] += 1

        # connect new junctions to path
        if segType == 'pTel':
            # segment becomes non telomeric as pos < jPos
            nodes[nodeChoice]["type"] = 'nonTel'
            nodes[nodeChoice]["WT"]   = str(uniqueID+1)

            # new WT connection
            nodes[uniqueID+1]["type"] = 'nonTel'
            nodes[uniqueID+1]["WT"]   = str(nodeChoice)

            # (new) telomeric segment unconnected
            nodes[uniqueID]["type"]        = 'pTel'
            nodes[uniqueID]["WT"]          = 'none'
            nodes[uniqueID]["M"]           = 'none'
            nodes[uniqueID]["centromeric"] = True

        elif segType == 'qTel':
            # segment becomes non telomeric as pos > jPos
            nodes[nodeChoice]["type"] = 'nonTel'
            nodes[nodeChoice]["WT"]   = str(uniqueID)

            # new WT connection
            nodes[uniqueID]["type"]   = 'nonTel'
            nodes[uniqueID]["WT"]     = str(nodeChoice)

            # (new) telomeric segment unconnected
            nodes[uniqueID+1]["type"]        = 'qTel'
            nodes[uniqueID+1]["WT"]          = 'none'
            nodes[uniqueID+1]["M"]           = 'none'
            nodes[uniqueID+1]["centromeric"] = True

        elif segType == 'nonTel':
            connID = int(nodes[nodeChoice].get("WT"))

            if jPos > nodes[connID].get("position"):
                nodes[connID]["WT"]     = str(uniqueID)
                nodes[uniqueID]["WT"]   = str(connID)

                nodes[uniqueID+1]["WT"] = str(nodeChoice)
                nodes[nodeChoice]["WT"] = str(uniqueID+1)

            elif jPos < nodes[connID].get("position"):
                nodes[connID]["WT"]     = str(uniqueID+1)
                nodes[uniqueID+1]["WT"] = str(connID)

                nodes[uniqueID]["WT"]   = str(nodeChoice)
                nodes[nodeChoice]["WT"] = str(uniqueID)

            # leave hasCent assignment for next cell cycle

    if verbose > 0:
        print("\nEntering subpath construction\npath: %s\n" %pathList.get(str(i)))
    ## end of introducing breakpoints

    # define subpaths:
    subPaths = []
    # populating list of lists from the newly introduced junctions
    # order does not matter as this is only for assigning copy number
    for ele in newJuncList:
        temp   = []
        temp.append(ele)
        nodeID = ele
        if verbose > 0:
            print("newJuncStart: %s" %ele)

        subPathCondition = True
        while subPathCondition:

            # check next connection (only WT)
            if nodes[nodeID].get("WT") != 'none':
                nodeID = int(nodes[nodeID].get("WT"))
                temp.append(nodeID)
                if verbose > 0:
                    print("Next connection (WT): %s" %nodeID)

                # check next connection (M)
                if nodes[nodeID].get("M") != 'none':
                    nodeID = int(nodes[nodeID].get("M"))
                    temp.append(nodeID)
                    if verbose > 0:
                        print("Next connection (M): %s" %nodeID)

                # if no muant connection, reached other junction
                else:
                    subPathCondition = False

            # no wild type; junction is telomeric
            else:
                # check
                telCondition = CheckBool.TelCheck(nodes,nodeID)
                if telCondition == True:
                    print("error: junction not telomeric but does not have WT")
                    sys.exit()

                subPathCondition = False

        if verbose > 0:
            print("temp: %s" %temp)
        subPaths.append(temp)

    if verbose > 0:
        print('Subpaths: ')
        print(subPaths)

    ## decide mitotic assignment and iterate along subpaths to delete
    # if two centromeres then 1 subpath will go to each daughter cell
    if nCent == 2:

        # randomly chooses which subpath is being assigned to 0 (deleted)
        # remaining subpath is kept (no code needed for this)
        subChoice = int(random.randint(0,1))

        # deletes chosen subpath
        for q in range( len( subPaths[subChoice] ) ):
            nodeID = subPaths[subChoice][q]
            nodes[nodeID]["cellID"] = 0
            nodes[nodeID]["cn"] = 0

    elif nCent > 2:
        # if more than two centromeres then stochastically assign the subpaths
        # between the two daughter cells

        for p in range(len(subPaths)):
            daughterCell = int(random.randint(0,1))

            for q in range( len( subPaths[p] ) ):

                if daughterCell == 0:
                    nodeID = subPaths[p][q]
                    nodes[nodeID]["cellID"] = daughterCell
                    nodes[nodeID]["cn"] = 0

    return nodes, DSBmat, nMitosisBreaks


def mitosis(nodes, pathList, cycleID, nCycles, centromerePos, DSBmat, nMitosisBreaks, verbose = 0):
    # assigns paths to daughter cells based on number of centromeres in the path
    if verbose > 0:
        print('\nEntering M\n')

    for i in range(len(pathList)):
        # randomly chooses daughter cell for assignment
        daughterCell = int(random.randint(0,1))
        # determines number of centromeres in path
        nCent, centList = CheckBool.checkCentromere(nodes, pathList, i, verbose)

        if nCent == 0:
        # stochastic assignment

            for j in range(len(pathList.get(str(i)))):
                nodeID  = pathList.get(str(i))[j]

                if daughterCell == 0:
                    nodes[nodeID]["cellID"] = daughterCell
                    nodes[nodeID]["cn"] = 0

        elif nCent == 1:
            # balanced assignment
            pass

        elif nCent > 1:
            # mitosis breakage
            nodes, DSBmat, nMitosisBreaks = cmplxSegregation(nodes, pathList, i, nCent, centList, centromerePos, DSBmat, nMitosisBreaks, verbose)


    return nodes, DSBmat, nMitosisBreaks


################################################################################
## Analysis Code:
# Generates summary statistics for final analysis
def sumStats(nodes, nChroms, nIns, nInv, cn_df, num, size, cycleID, DSBmat, nBiasedChroms, nMitosisBreaks, write_cicos = False, write_shatterseek = False, write_sumStats = False):
    sumStats_total = pd.DataFrame(columns=["nDSB", "nDel", "nInv", "nIns", "nDup", 'cycleID', 'nBiasedChroms', 'nMitosisBreaks'])
    sumStats_chrom = pd.DataFrame(columns=["chr", "nDSB", "nOsc", "nDel", "nIns", "nInv", "nDup"])

    ## code for merging segments for oscillating cn statistic
    # create merged haplotype data frame
    cn_temp = {}

    # create merged cn data frame
    cn_df_merged = {}

    # initialisng deletions summary statistic
    nDel = [ 0 for i in range(nChroms)]

    # initialisng duplications summary statistic
    nDup = [ 0 for i in range(nChroms)]

    # merge haplotypes, maintain segment size
    for i in range(nChroms):

        # initialise list
        cn_temp[str(i+1)] = []

        # populate list with total cn
        for j in range(num[i]):

            # taking data from cirosPlot class, duplications method
            s = cn_df[i].get('A')[j][0]
            e = cn_df[i].get('A')[j][1]
            c = cn_df[i].get('A')[j][2] + cn_df[i].get('B')[j][2]

            cn_temp[str(i+1)].append( [s, e, c] )

    # merge segments based on cn
    for i in range(nChroms):

        # construct list for appending
        idx = str(i+1)
        cn_df_merged[str(i+1)] = []

        # merge segments of same cn
        for j in range(num[i]):
            # firt element
            if j == 0:
                seg_start = cn_temp.get(idx)[j][0]
                seg_cn    = cn_temp.get(idx)[j][2]

            # same cn, non final element
            elif j != 0 and j != num[i]-1 and cn_temp.get(idx)[j][2] == seg_cn :
                pass

            # cn change, non final element
            elif j != 0 and j != num[i]-1 and cn_temp.get(idx)[j][2] != seg_cn :
                # complete segment and store
                seg_end = cn_temp.get(idx)[j-1][1]
                cn_df_merged[idx].append( [seg_start, seg_end, seg_cn] )

                # start next segment
                seg_start = cn_temp.get(idx)[j][0]
                seg_cn    = cn_temp.get(idx)[j][2]

            # same cn, final element
            elif j != 0 and j == num[i]-1 and cn_temp.get(idx)[j][2] == seg_cn:
                # complete segment and store
                seg_end = cn_temp.get(idx)[j-1][1]
                cn_df_merged[idx].append( [seg_start, seg_end, seg_cn] )

            # cn change, final element
            elif j != 0 and j == num[i]-1 and cn_temp.get(idx)[j][2] != seg_cn :
                # complete segment and store
                seg_end = cn_temp.get(idx)[j-1][1]
                cn_df_merged[idx].append( [seg_start, seg_end, seg_cn] )


    # writing SV deletions & duplications for shatterseek and circos
    for i in range(nChroms):
        idx = str(i+1)
        for j in range(len(cn_df_merged[idx])):

            # if deletion on a haplotype, cn < 2
            if cn_df_merged.get(idx)[j][2] < 2:

                # get location:
                s1 = cn_df_merged.get(idx)[j][0]

                # write SV deletions - for Circos (by haplotype)
                # CN deletions/duplications written for Circos in circosPlot method
                if write_cicos:
                    with open('../output/circos/sv_data.tsv', 'a', newline='') as file:
                        writer = csv.writer(file, delimiter = '\t')
                        # key: [chr, start, '+', chr, end, '-', 'svtype=DEL', cycleNum]
                        writer.writerow([i+1, s1, '+', i+1, s1, '-', 'svtype=DEL', cycleID])

                # number of deletions gets updated each time chrom is called (either hapA or hapB)
                nDel[i] += 1

            # number of duplications gets updated each time chrom is called (either hapA or hapB)
            elif cn_df_merged.get(idx)[j][2] > 2:
                nDup[i] += 1


            # write SV duplications - for shatterseek
            if cn_df_merged.get(idx)[j][2] > 2 and cycleID == 1:

                s1 = cn_df_merged.get(idx)[j][0]
                e1 = cn_df_merged.get(idx)[j][1]

                if write_shatterseek:
                    with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                        writer = csv.writer(file, delimiter = '\t')
                        # key: [chr1, start, '-', chr1, end, '+', "DUP"]
                        writer.writerow([i+1, s1, '-', i+1, e1, '+', "DUP"])

            # write SV deletions - for shatterseek
            if cn_df_merged.get(idx)[j][2] < 2 and cycleID == 1:

                s1 = cn_df_merged.get(idx)[j][0]
                e1 = cn_df_merged.get(idx)[j][1]

                if write_shatterseek:
                    with open('../output/ShatterSeek/R/SVData.tsv', 'a', newline='') as file:
                        writer = csv.writer(file, delimiter = '\t')
                        # key: [chr1, start, '+', chr1, end, '-', "DEL"]
                        writer.writerow([i+1, s1, '+', i+1, e1, '-', "DEL"])


    # calculate nOsc
    nOsc = [ 0 for i in range(nChroms)]
    for i in range(nChroms):
        # oscillations are counted as the change, not the segments themselves
        # thus nOsc = nSegments - 1
        nOsc[i] = len(cn_df_merged.get(str(i+1)))-1


    # write CN data to tsv - for ShatterSeek
    for i in range(nChroms):
        idx = str(i+1)
        for j in range(len(cn_df_merged.get(idx))):

            chr1   = i+1
            start  = cn_df_merged.get(idx)[j][0]
            end    = cn_df_merged.get(idx)[j][1]
            cn_tot = cn_df_merged.get(idx)[j][2]

            if write_shatterseek:
                with open('../output/ShatterSeek/R/CNData.tsv', 'a', newline='') as file:
                    writer = csv.writer(file, delimiter = '\t')
                    writer.writerow([chr1, start, end, cn_tot])

    for i in range(nChroms):
        sumStats_chrom.loc[i] = [i+1, DSBmat[i][0]+DSBmat[i][1], nOsc[i], nDel[i], nIns[i][0]+nIns[i][1], nInv[i][0]+nInv[i][1], nDup[i]]
    # write summary statistics for sumstats inference
    if write_sumStats:
        print("writing summary statistics for each chromosome")
        for i in range(nChroms):
            with open('../output/sumstats/sumStats_chrom.tsv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter = '\t')
                writer.writerow([i+1, DSBmat[i][0]+DSBmat[i][1], nOsc[i], nDel[i], nIns[i][0]+nIns[i][1], nInv[i][0]+nInv[i][1], nDup[i]])

    DSB_tot = 0; nDel_tot = 0; nIns_tot = 0; nInv_tot = 0; nDup_tot = 0
    for i in range(nChroms):
        DSB_tot  += (DSBmat[i][0]+DSBmat[i][1])
        nDel_tot += nDel[i]
        nIns_tot += (nIns[i][0]+nIns[i][1])
        nInv_tot += (nInv[i][0]+nInv[i][1])
        nDup_tot += nDup[i]

    sumStats_total.loc[1] = [DSB_tot, nDel_tot, nIns_tot, nInv_tot, nDup_tot, cycleID, nBiasedChroms, int(nMitosisBreaks)]
    if write_sumStats:
        print("writing summary statistics for all chromosomes")
        with open('../output/sumstats/sumStats_total.tsv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter = '\t')
            writer.writerow([DSB_tot, nDel_tot, nIns_tot, nInv_tot, nDup_tot, cycleID, nBiasedChroms, int(nMitosisBreaks)])

    return sumStats_chrom, sumStats_total


def analysis(nodes, nCycles, cycleID, lmbda, chromLengths, DSBmat, cn_df, num, size, nChroms, nBiasedChroms, nMitosisBreaks, write_cicos = False, write_shatterseek = False, write_sumStats = False):
    # create files for writing to
    if cycleID == 0 and write_cicos:

        with open('../output/circos/sv_data.tsv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter = '\t')
            writer.writerow(["chr1", "coord1", "strand1", "chr2", "coord2", "strand2",	"extra", "cycleNum"])

        with open('../output/circos/cn_data.tsv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter = '\t')
            writer.writerow(["chr", "start", "end", "extra", "cycleNum"])


    if cycleID == 0: #nCycles-1:

        if write_sumStats:
            print("Writing summary statistics to files")
            # summary statistics for the whole system
            with open('../output/sumstats/sumStats_total.tsv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter = '\t')
                writer.writerow(["nDSB", "nDel", "nInv", "nIns", "nDup", 'cycleID', 'nBiasedChroms', 'nMitosisBreaks'])

            # summary statistics for each chromosome
            with open('../output/sumstats/sumStats_chrom.tsv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter = '\t')
                writer.writerow(["chr", "nDSB", "nOsc", "nDel", "nIns", "nInv", "nDup"])

        if write_shatterseek:
            # for use of shatterseek chromothripsis determination
            with open('../output/ShatterSeek/R/SVData.tsv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter = '\t')
                writer.writerow(["chrom1", "start1", "strand1", "chrom2", "end2", "strand2", "svclass"])

            with open('../output/ShatterSeek/R/CNData.tsv', 'w', newline='') as file:
                writer = csv.writer(file, delimiter = '\t')
                writer.writerow(["chromosome", "start", "end", "total_cn"])


    # analyse data for SVs
    nIns  = calcSVs.insertions(nodes,cycleID, write_cicos = write_cicos, write_shatterseek = write_shatterseek)
    nInv  = calcSVs.inversions(nodes,cycleID,chromLengths, write_cicos = write_cicos, write_shatterseek = write_shatterseek)
    cn_df, num = calcSVs.duplications(nodes,cycleID,nChroms,chromLengths,cn_df,num,size, write_cicos = write_cicos, write_shatterseek = write_shatterseek)


    # generate summary statistics in final cell cycle
    sumStats_total = pd.DataFrame(columns=["nDSB", "nDel", "nInv", "nIns", "nDup", 'cycleID', 'nBiasedChroms', 'nMitosisBreaks'])
    sumStats_chrom = pd.DataFrame(columns=["chr", "nDSB", "nOsc", "nDel", "nIns", "nInv", "nDup"])

    if cycleID == nCycles-1:
        sumStats_chrom, sumStats_total = sumStats(nodes, nChroms, nIns, nInv, cn_df, num, size, cycleID, DSBmat, nBiasedChroms, nMitosisBreaks, write_cicos, write_shatterseek, write_sumStats)

    return sumStats_chrom, sumStats_total

################################################################################
# generate SV:
def main(matType = 'biased', lmbda = 5, minDSB = 0, maxDSB = 40, nCycles = 2, write_cicos = False, write_shatterseek = False, write_sumStats = False, verbose = 0):

    # variables
    nChroms  = 22
    nodes    = []
    pathList = {}

    # import chromosome lengths
    chromLengths = pd.read_csv("../input/hg38.size.tsv", header=None, sep='\t')

    # define centromere positions
    centromerePos = []
    for length in range(len(chromLengths)):
        centromerePos.append( chromLengths[1][length] / 2 )

    # initialise the number of DSBs on each chromosome
    DSBmat = [ [0,0] for i in range(nChroms)]

    # initialise the number of breaks at mitosis
    nMitosisBreaks = 0

    # define matrix preferencing chromosomes
    # commented out by lbx
    # #matType = 'random'
    # matType = 'biased'
    # #matType = 'fixed'
    chromMat, nBiasedChroms = matPref(matType, nChroms)

    # parameters
    # commented out by lbx
    # lmbda   = 5    # max number of unrepaired segments a cell can handle
    # nCycles = 2    # number of cell cycles

    # determine segment size of cn_df
    size = int(50E5)

    # cell cycles
    cycleID = 0
    count   = 0

    for i in range(nCycles):
        if verbose > 0:
            print("\n############################ ")

        # for selecting specific DSB ranges/values by cell cycle number
        # commented out by lbx
        # if cycleID == 0:
        #     minDSB  = 0
        #     maxDSB  = 40
        # else:
        #     minDSB  = 0
        #     maxDSB  = 40

        # generate breakpoints
        nDSB = generateDSBs(minDSB, maxDSB)
        if verbose > 0:
            print("Cycle: %d; Number of DSBs: %d" %(cycleID, nDSB))
f

        if nDSB > 0:
            # counts number of events
            count += 1

            # junction cn initialisation; event = insertion of DSBs
            if count == 1:
                firstEvent = True
            else: firstEvent = False
        else: firstEvent = False


        # initialises nodes dictionary
        nodes, DSBmat = generateNodes(nodes, nDSB, nChroms, chromLengths, firstEvent, chromMat, DSBmat)
        if verbose > 0:
            print("Total number of junctions in nucleus: %d\n" %len(nodes))


        # define path ends
        nodes = generateTelomeres(nodes)


        # growth phase
        nodes = g1(nodes, lmbda, verbose)


        # assign centromeres to segments
        nodes = generateCentromeres(nodes, centromerePos)


        # path construction
        pathList = connectedPathConstruction(nodes, pathList, verbose)
        telomeric, nonTelomeric = unconnectedPathConstruction(nodes, verbose)


        # synthesis & second growth phase
        nodes, pathList = syn_g2(nodes, pathList, telomeric, nonTelomeric, verbose)


        # path directionality
        nodes = checkInv(nodes, pathList)


        # mitosis phase
        nodes, DSBmat, nMitosisBreaks = mitosis(nodes, pathList, cycleID, nCycles, centromerePos, DSBmat, nMitosisBreaks, verbose)


        # initialise cn information
        cn_df, num, size = cnProfiles(nChroms, chromLengths, size)


        # open output file for writing SV data
        sumStats_chrom, sumStats_total = analysis(nodes, nCycles, cycleID, lmbda, chromLengths, DSBmat, cn_df, num, size, nChroms, nBiasedChroms, nMitosisBreaks, write_cicos, write_shatterseek, write_sumStats)


        # end of cycle cleaning:
        cycleID += 1

        cn_df.clear()
        pathList.clear()
    nodes.clear()

    if verbose > 0:
        print("\n~~ End of Simulation ~~\n")
    return sumStats_chrom, sumStats_total


if __name__ == '__main__':
    print(" Running SVGen.\n")
    main()
