import math
import copy

def main():
        
        funcs = { 1 : rateOfGrowthBookValue,
                  2 : rateOfGrowthNetIncome,
                  3 : intrisicValueBookValueMethod,
                  4 : intrisicValueCashFlowMethod,
                  5 : shouldYouSell }
        
        while(True):
                print("\n\t** Options **\n")
                print("\t1. Rate Of Growth by Book Value")
                print("\t2. Rate Of Growth by Net Income")
                print("\t3. Intrisic Value by Book Value & Dividend")
                print("\t4. Intrisic Value by Free Cash Flows (i.e. Owner's Earnings)")
                print("\t5. Should you sell")
                print("\t6. Quit")
                opt = int(input("-> "))

                if(opt == 6):
                        break
                else:
                        funcs[opt]()
                        

def rateOfGrowthBookValue():
        
        # Collect Input
        cbv = float(input("\nCurrent Book Value: "))
        obv = float(input("Old Book Value: "))
        years = float(input("Years Between Book Value: "))
        
        # Compute
        upper = 1/years
        base = cbv /obv
        a    = pow(base, upper)
        print("Book Value's Growth Rate: {0}".format(100*(a-1)))

def rateOfGrowthNetIncome():
        
        
        # Collect Input
        cbv = float(input("\nCurrent Net Income: "))
        obv = float(input("Old Net Income: "))
        years = float(input("Years Between Net Income: "))
        
        # Compute
        upper = 1/years
        base = cbv /obv
        a    = pow(base, upper)
        print("Net Income's Growth Rate: {0}".format(100*(a-1)))

def intrisicValueBookValueMethod():

        # Constraints
        print("\nThis method is better for:")
        print("      1. Have Low Debt 0.50$ for each 1$ of Equity")
        print("            1.1 0.50$ of Debt for each 1$ of Equity")
        print("      2. Has a long-term competitive advantadge")
        print("      3. Company that have been growing at stable pace")
        print("      4. Have stable & vigilant leaders")
        print("      5. Estimates may become unrealistic beyond 13% growth rate")
        print("      6. Not have a high-degree of share-buyback")
        print("      7. Didnt have Stock splits during the years analysed\n")

        print(" What to proceed ?")
        opt = str(input("-> "))
        if(opt != "y" or opt != "yes"):
                return

        # Collect Input
        coupon = float(input("\nCash Taken Out Of Business: ")) # Cash Taken Out of Business
        par    = float(input("Current Book Value: ")) # Current Book Value
        year   = float(input("Numbers of Years: "))
        r      = float(input("10 Year Federal Note: "))
        bvc    = float(input("Average Percent Book Value Change Per Year: "))

        # Compute
        perc = (1+bvc/100)
        base = pow(perc,year)
        parr = par*base
        r    = r/100
        extra= pow((1+r),year)
        val  = coupon * (1-(1/extra))/r+parr/extra;

        print("Intrisic Value: {0}".format(str(val)))

def shouldYouSell():
        csp = float(input("Current Selling Price: "))
        ns  = int(input("Number of Shares: "))
        cdr = float(input("What annual discount rate makes the intrinsic value equal to the market price for the stock you currently own: "))
        cg  = float(input("What will be the capital gains tax rate if you decide to sell your current stock: "))
        g   = float(input("What gains have you made while owning your current stock pick: "))
        ndr = float(input("For the new stock pick, what annual discount rate makes the intrinsic value equal to the market price: "))

        stock_new = list()
        stock_current = list()

        stock_current.append(round(csp * ns,2))
        stock_new.append(round(stock_current[0] - cg * g, 2))

        for i in range(5,35,5):
                stock_current.append(round(stock_current[0] * pow(1 + cdr, i),2))
                stock_new.append(round(stock_new[0] * pow(1 + ndr, i),2))

        print(" |    Current Stock    |    New Stock    |")
        for i in range(0,7):
                print(" |    {0}    |    {1}    |".format(stock_current[i], stock_new[i]))


def intrisicValueCashFlowMethod():
        
        print("\nThis method is better for:")
        print("      1. High growth Companies")
        print("      2. Companies have had a large number of share buy-backs")

        # Compute Average FCF
        fcfs = list(str(input("\nAll FCF separated by comas: ")).split(","))
        fcfs = [float(x.replace("(","").replace(")","")) for x in fcfs]
        fcf  = sum(fcfs)/len(fcfs)
        print("Average FCF: {0}".format(fcf))

        # Compute FCF future estimates
        growth = float(input("\nGrowth Rate: "))
        years  = int(input("Years to Analyse: "))
        grown_fcfs = [round((fcf*pow(1+growth,i)),2) for i in range(1,years+1)]
        print("Estimated FCFs: {0}".format(grown_fcfs))

        # Discout Future Estimates
        interest_rate = float(input("\nInterest Rate as Float: "))
        interest = [round(float(pow(1.0+interest_rate,x)),2) for x in range(1,years+1)]
        print("Future Interest: {0}".format(interest))
        dis_fcfs = [round(fc/interest,2) for fc,interest in zip(grown_fcfs,interest)]
        print("Discounted Estimated FCFs: {0}".format(dis_fcfs))
        print("Sum of DFCF: {0}".format(sum(dis_fcfs)))

        # Count to Perpetuity
        long_growth = float(input("\nLong Term Growth Rate: "))
        shares = int(input("Outstanding Shares (Careful with millions and thousands): "))

        # Variables
        year = years+1
        growth = 1.0+growth
        long_growth = 1.0+long_growth
        interest = 1.0+interest_rate

        # Display Variables
        print("FCF: {0}".format(fcf))
        print("Long Growth: {0}".format(long_growth))
        print("Years: {0}".format(year))
        print("Interest: {0}".format(interest))

        # Calculate Perpetuity FCF
        pfcf = fcf * pow(growth,year) * long_growth / (interest-long_growth) * 1.0 / pow(interest,year)
        print("Perpetuity FCF: {0}".format(round(pfcf,2)))

        # Total & Share Intrisic Value
        total = sum(dis_fcfs) + pfcf
        print("Total FCF: {0}".format(round(total,2)))
        value = total / shares
        print("Intrisic Value Per Share: {0}".format(value))

        # Find Current Interest
        #current = float(input("Current market price: "))
        #if(abs(current-value) > 0.011):
        #        eps = 0.0001
        #        for i in range(1,50):
        #                xa = float(i / 100)
        #                xb = float(i / 100)
        #                counter = 0
        #                flag = 0
        #                while(flag == 0):
        #                        xa = xb
        #                        xb = fndr(fcf, long_growth, growth, years, current, shares, xa)
        #                        counter += 1
        #                        if not(abs(xb - xa) > eps and counter < 30 and abs(xb - xa) < 1):
        #                                flag = 1
        #                if(abs(xb - xa) <= eps):
        #                        print("Current Annual return: {0}".format(xb*100))

def fndr(byfcf, lgr, gr, n, mp, cso, x):
        b = byfcf
        l = lgr - 1.0
        gr1 = gr
        x1 = 1 + x
        m = n + 1
        r = pow(gr1, m)
        f0 = b * r * (1 + l) / (x - l) / pow(x1, m) + b * (1 - pow(gr1 / x1, m)) / (1 - gr1 / x1) - b - mp * cso
        fder = -b * (1 + l) * r * (1 / pow(x1, m) / pow(-l + x, 2) + m * pow(x + 1, -1 - m) / (-l + x)) + b * (m * r * pow(x1, -1 - m) / (1 - gr1 / x1) - gr1 * (1 - r / pow(x1, m)) / pow((1 - gr1 / x1) * x1, 2))
        result = x - f0 / fder
        return result

main()
