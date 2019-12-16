from SymbolArray import SymbolArray
from FormulaSpec import FormulaGenerator as FG, Formula as Formula
import logging


class FormulaPopulation:
    def __init__(self, popSize, paramDict={}):
        self.popSize = popSize
        self.paramDict = paramDict #dictionary- VarName key: {lower bound, upper bound}
        self.formulaGen = FG.FormulaGenerator #class to generate formula sets

        self.population = [] #arrayList of formulas
        self.fitness = None
        self.model1 = None
        self.model2 = None
        self.lowerBound = {} #hashmap of key value pairs string, double
        self.upperBound = {} #hashmap of key value pairs string, double

        self.parameters = SymbolArray()
        #store = new FastStore();

        self.variables = [] #arrayList of strings

        #operators = new FormulaGenOps(this, parameters);
        #bestSolutions = new TreeSet < Solution > ();
        #setFitness(GeneticOptions.fitness_type);

    #Add variables to formula pop store
    def addVariable(self, v, lower, upper):
        #store.addVariable(V, 0);
        self.variables.append(v)
        self.lowerBound[v] = lower
        self.upperBound[v] = upper

    def addGeneticInitFormula(self, genOps):
        #Generate initial atomic formulas of G, F, U for each variable
        #Creates formulas with no params, just rule structure
        self.population = self.formulaGen.atomicGeneticFormula(self.formulaGen, variables=self.variables, genOps=genOps)

        self.logFormulas(self.population, "Initial")



    def logFormulas(self, pop, type):
        logging.info(type + " Formula Population:")

        for f in pop:
            logging.info('%s' % (f.toString()))
