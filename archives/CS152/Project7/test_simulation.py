# Huan Bui
# Fall 2017
# CS 152 Project 7
#
# test of Simulation class
import sys
import simulation

# main test function, expects one command line argument which is percent darted
def main(argv):
    if len(argv) < 2:
        print( "Usage: python %s <perc darted>" % (argv[0]) )
        exit(-1)

    # create a simulation using the default parameters
    sim = simulation.Simulation()

    # set the percent darted
    sim.setPercDart( float(argv[1]) )
    sim.setCullStrategy( float(argv[2]) )

    # print(sim.getCullStrategy())

    # run the simulation
    results = sim.runSimulation(200)

    # average some of the results
    avgpop = 0.0
    avgcalf = 0.0
    avgJuv = 0.0
    avgadtF = 0.0
    avgadtM = 0.0
    avgSen = 0.0
    avgcull = 0.0
    for item in results:
        avgpop += item[0]
        avgcalf += item[1]
        avgJuv += item[2]
        avgadtM += item[3]
        avgadtF += item[4]
        avgSen += item[5]
        avgcull += item[6]
        
    avgpop /= len(results)
    avgcalf /= len(results)
    avgJuv /= len(results)
    avgadtM /= len(results)
    avgadtF /= len(results)
    avgSen /= len(results)
    avgcull /= len(results)

    print("Cull Strategy:", sim.getCullStrategy())
    print("Darted: ", sim.getPercDart())
    print("Total: ", int(avgpop))
    print("Calves: ", int(avgcalf))
    print("Juveniles: ", int(avgJuv))
    print("Adult Males: ", int(avgadtM))
    print("Adult Females: ", int(avgadtF))
    print("Seniors: ", int(avgSen))
    print("Num Culled: ", int(avgcull))

    sim.writeDemographics("demographics.csv")

if __name__ == "__main__":
    main(sys.argv)
