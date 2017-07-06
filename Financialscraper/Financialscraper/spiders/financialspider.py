
# -*- coding: utf-8 -*-
import scrapy
import useragent
from scrapy.http import Request, FormRequest
from Financialscraper.items import FinancialscraperItem
from Financialscraper.items import GetincomestatementItem
from Financialscraper.items import GetbalancesheetItem
from Financialscraper.items import GetcashflowItem
import time, datetime, csv, random, base64, re
from time import sleep


class FinancialspiderSpider(scrapy.Spider):
    name = "financialspider"
    allowed_domains = ["uk.investing.com"]
    start_urls = (
        'http://www.uk.investing.com/',
    )

    select_param = ""
    useragent_lists = useragent.user_agent_list

    def __init__(self,  param ='None', *args, **kwargs):

        super(FinancialspiderSpider, self).__init__(*args, **kwargs)
        
        self.select_param = param

    def set_proxies(self, url, callback):

        req = Request(url=url, callback=callback, dont_filter=True)
        user_pass=base64.encodestring(b'user:password').strip().decode('utf-8')
        req.meta['proxy'] = "http://xxx.xxx.net:xxx"
        req.headers['Proxy-Authorization'] = 'Basic ' + user_pass
        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        req.headers['User-Agent'] = user_agent

        return req

    def start_requests(self):

        self.clearLog()
        self.makeLog("=================== Start ===================")

        # Check param
        if (self.select_param!="annual" and self.select_param!="quarterly"):
            print(" ================ Please Insert Correct Mode!!! ================ ")
            print(" * Annual    : scrapy crawl financialspider -a param=annual ")
            print(" * Quarterly : scrapy crawl financialspider -a param=quarterly ")
            return  

        # read varid from csv file
        myfile = open("symbolUrl_lists.csv", "rb")
        urlLists = csv.reader(myfile)

        for url in urlLists:

            url=''.join(url).strip()
            variable = url.split("/")[-1]
            req = self.set_proxies(url, self.getPairID)
            req.meta['variable'] = variable
            req.meta['url'] = url
            yield req   

            # return

    def getPairID(self, response):

        self.logger.info("============= getPairID ===============")

        symbid = ''.join(response.xpath('//div[@id="js_instrument_chart_wrapper"]/@data-pair_id').extract()).strip()
        variable = response.meta['variable']
        base_url = response.meta['url']

        item = FinancialscraperItem()

        item['variable'] = variable
        item['url'] = base_url
        item['symbid'] = symbid
        if self.select_param == "annual":
            item['Freq'] = "1"
        elif self.select_param == "quarterly":
            item['Freq'] = "2"

        yield item

        pairidTXT = ''.join(response.xpath('//table[@class="genTbl closedTbl exchangeDropdownTbl displayNone"]/tbody/tr[2]/@data-href').extract()).strip()
        pair_ID = pairidTXT.split("=")[-1]
        pair_ID1 = symbid

        # Annual        
        if self.select_param == "annual":
            
            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=INC&period_type=Annual"%pair_ID
            req = self.set_proxies(url, self.getIncomeStatement)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=INC&period_type=Annual"%pair_ID1
            req = self.set_proxies(url, self.getIncomeStatement)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=BAL&period_type=Annual"%pair_ID
            req = self.set_proxies(url, self.getBalanceSheet)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=BAL&period_type=Annual"%pair_ID1
            req = self.set_proxies(url, self.getBalanceSheet)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req


            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=CAS&period_type=Annual"%pair_ID
            req = self.set_proxies(url, self.getCashFlow)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=CAS&period_type=Annual"%pair_ID1
            req = self.set_proxies(url, self.getCashFlow)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "1"
            req.meta['url'] = base_url

            yield req

        # Quarterly        
        elif self.select_param == "quarterly":

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=INC&period_type=Interim"%pair_ID
            req = self.set_proxies(url, self.getIncomeStatement)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=INC&period_type=Interim"%pair_ID1
            req = self.set_proxies(url, self.getIncomeStatement)

            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=BAL&period_type=Interim"%pair_ID
            req = self.set_proxies(url, self.getBalanceSheet)
            
            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=BAL&period_type=Interim"%pair_ID1
            req = self.set_proxies(url, self.getBalanceSheet)
            
            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=CAS&period_type=Interim"%pair_ID
            req = self.set_proxies(url, self.getCashFlow)
            
            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req    

            url = "https://uk.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID=%s&report_type=CAS&period_type=Interim"%pair_ID1
            req = self.set_proxies(url, self.getCashFlow)
            
            req.meta['symbid'] = symbid
            req.meta['freq'] = "2"
            req.meta['url'] = base_url

            yield req 

    def getIncomeStatement(self, response):

        self.logger.info("============= getIncomeStatement ===============")
        item = GetincomestatementItem()

        base_url = response.meta['url']
        symbid = response.meta['symbid']
        freq = response.meta['freq']

        item['Symb'] = symbid
        item['Freq'] = freq

        count = 1
        datePaths = response.xpath('//tr[@class="alignBottom"]/th')
        for datePath in datePaths:

            dateYear = ''.join(datePath.xpath('span[@class="bold"]/text()').extract()).strip()
            dateDay = ''.join(datePath.xpath('div[@class="noBold arial_11"]/text()').extract()).strip()

            if dateYear and dateDay:

                self.logger.info("--------------------------------")
                date = dateDay + "/" + dateYear
                item['Date'] = date

                totalRevenue = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Revenue'] = totalRevenue

                revenue = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[@class='child']/td[%s]/text()"%(count+1)).extract_first() 
                item['Revenue'] = revenue

                otherRevenueTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[@class='child last']/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Revenue_Total'] = otherRevenueTotal

                costofRevenueTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Cost_of_Revenue_Total'] = costofRevenueTotal

                grossProfit = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Gross_Profit'] = grossProfit

                totalOperatingExpenses = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Operating_Expenses'] = totalOperatingExpenses

                sellingGeneralAdminExpensesTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Selling_General_Admin_Expenses_Total'] = sellingGeneralAdminExpensesTotal

                researchDevelopment = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Research_Development'] = researchDevelopment

                depreciationAmortization = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Depreciation_Amortization'] = depreciationAmortization

                interestExpenseIncomeNetOperating = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Interest_Expense_Income_Net_Operating'] = interestExpenseIncomeNetOperating

                unusualExpenseIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Unusual_Expense_Income'] = unusualExpenseIncome

                otherOperatingExpensesTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Operating_Expenses_Total'] = otherOperatingExpensesTotal

                operatingIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first()
                item['Operating_Income'] = operatingIncome

                interestIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]/td[%s]/text()"%(count+1)).extract_first()
                item['Interest_Income_Expense_Net_Non_Operating'] = interestIncome

                gainLoss = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[9]/td[%s]/text()"%(count+1)).extract_first()
                item['Gain_Loss_on_Sale_of_Assets'] = gainLoss

                otherNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Net'] = otherNet

                netIncomeBeforeTaxes = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[11]/td[%s]/text()"%(count+1)).extract_first()
                item['Net_Income_Before_Taxes'] = netIncomeBeforeTaxes

                provisionIncomeTaxes = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[12]/td[%s]/text()"%(count+1)).extract_first()
                item['Provision_for_Income_Taxes'] = provisionIncomeTaxes

                netIncomeAfterTaxes = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[13]/td[%s]/text()"%(count+1)).extract_first()
                item['Net_Income_After_Taxes'] = netIncomeAfterTaxes

                minorityInterest = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[14]/td[%s]/text()"%(count+1)).extract_first()
                item['Minority_Interest'] = minorityInterest

                equityInAffiliates = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[15]/td[%s]/text()"%(count+1)).extract_first()
                item['Equity_In_Affiliates'] = equityInAffiliates

                USGAAPAdjustment = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[16]/td[%s]/text()"%(count+1)).extract_first()
                item['US_GAAP_Adjustment'] = USGAAPAdjustment

                netIncomeBeforeExtraordinaryItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[17]/td[%s]/text()"%(count+1)).extract_first()
                item['Net_Income_Before_Extraordinary_Items'] = netIncomeBeforeExtraordinaryItems

                totalExtraordinaryItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[18]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Extraordinary_Items'] = totalExtraordinaryItems

                netIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[19]/td[%s]/text()"%(count+1)).extract_first()
                item['Net_Income'] = netIncome

                totalAdjustmentsNetIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[20]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Adjustments_to_Net_Income'] = totalAdjustmentsNetIncome

                incomeAvailableCommonExcludingExtraordinaryItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[21]/td[%s]/text()"%(count+1)).extract_first()
                item['Income_Available_to_Common_Excluding_Extraordinary_Items'] = incomeAvailableCommonExcludingExtraordinaryItems

                dilutionAdjustment = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[22]/td[%s]/text()"%(count+1)).extract_first()
                item['Dilution_Adjustment'] = dilutionAdjustment

                dilutedNetIncome = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[23]/td[%s]/text()"%(count+1)).extract_first()
                item['Diluted_Net_Income'] = dilutedNetIncome

                dilutedWeightedAverageShares = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[24]/td[%s]/text()"%(count+1)).extract_first()
                item['Diluted_Weighted_Average_Shares'] = dilutedWeightedAverageShares

                dilutedEPSExcludingExtraordinaryItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[25]/td[%s]/text()"%(count+1)).extract_first()
                item['Diluted_EPS_Excluding_Extraordinary_Items'] = dilutedEPSExcludingExtraordinaryItems

                dPSCommonStockPrimaryIssue = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[26]/td[%s]/text()"%(count+1)).extract_first()
                item['DPS_Common_Stock_Primary_Issue'] = dPSCommonStockPrimaryIssue

                dilutedNormalizedEPS = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[27]/td[%s]/text()"%(count+1)).extract_first()
                item['Diluted_Normalized_EPS'] = dilutedNormalizedEPS

                count = count + 1

                yield item
        if count>1:                
            log_txt = base_url + ", IncomeStatement, " + self.select_param        
            self.makeLog(log_txt)

                # return

    def getBalanceSheet(self, response):

        self.logger.info("============= getBalanceSheet ===============")

        item = GetbalancesheetItem()


        base_url = response.meta['url']
        symbid = response.meta['symbid']
        freq = response.meta['freq']

        item['Symb'] = symbid
        item['Freq'] = freq

        count = 1
        datePaths = response.xpath('//tr[@class="alignBottom"]/th')
        for datePath in datePaths:

            dateYear = ''.join(datePath.xpath('span[@class="bold"]/text()').extract()).strip()
            dateDay = ''.join(datePath.xpath('div[@class="noBold arial_11"]/text()').extract()).strip()

            if dateYear and dateDay:


                self.logger.info("--------------------------------")
                date = dateDay + "/" + dateYear
                item['Date'] = date

                TotalCurrentAssets = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Current_Assets'] = TotalCurrentAssets
                # self.logger.info(TotalCurrentAssets)

                CashandShortTermInvestments = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first() 
                item['Cashand_Short_Term_Investments'] = CashandShortTermInvestments

                Cash = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first() 
                item['Cash'] = Cash

                CashEquivalents = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first() 
                item['Cash_Equivalents'] = CashEquivalents

                ShortTermInvestments = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first() 
                item['Short_Term_Investments'] = ShortTermInvestments

                TotalReceivablesNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Receivables_Net'] = TotalReceivablesNet    

                AccountsReceivablesTradeNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first() 
                item['Accounts_Receivables_TradeNet'] = AccountsReceivablesTradeNet

                TotalInventory = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Inventory']  = TotalInventory

                PrepaidExpenses = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[8]/td[%s]/text()"%(count+1)).extract_first() 
                item['Prepaid_Expenses'] = PrepaidExpenses

                OtherCurrentAssetsTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]//table/tbody/tr[9]/td[%s]/text()"%(count+1)).extract_first() 
                item['Other_Current_Assets_Total'] = OtherCurrentAssetsTotal

                TotalAssets = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]/td[%s]/text()"%(count+1)).extract()[1]
                # self.logger.info(TotalAssets)
                item['Total_Assets'] = TotalAssets

                PropertyPlantEquipmentTotalNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Property_Plant_Equipment_Total_Net'] = PropertyPlantEquipmentTotalNet

                PropertyPlantEquipmentTotalGross = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Property_Plant_Equipment_Total_Gross'] = PropertyPlantEquipmentTotalGross

                AccumulatedDepreciationTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Accumulated_Depreciation_Total'] = AccumulatedDepreciationTotal

                GoodwillNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Goodwill_Net'] = GoodwillNet

                IntangiblesNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Intangibles_Net'] = IntangiblesNet

                LongTermInvestments = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                item['Long_Term_Investments'] = LongTermInvestments

                NoteReceivableLongTerm = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first()
                item['Note_Receivable_Long_Term'] = NoteReceivableLongTerm

                OtherLongTermAssetsTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[8]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Long_Term_Assets_Total'] = OtherLongTermAssetsTotal

                OtherAssetsTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]//table/tbody/tr[9]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Assets_Total'] = OtherAssetsTotal

                TotalCurrentLiabilities = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[5]/td[%s]/text()"%(count+1)).extract()[2]
                # self.logger.info(TotalCurrentLiabilities)
                item['Total_Current_Liabilities']  = TotalCurrentLiabilities

                AccountsPayable = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Accounts_Payable'] = AccountsPayable

                PayableAccrued = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Payable_Accrued'] = PayableAccrued

                AccruedExpenses = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Accrued_Expenses'] = AccruedExpenses

                NotesPayableShortTermDebt = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Notes_Payable_Short_Term_Debt'] = NotesPayableShortTermDebt

                CurrentPortofLTDebtCapitalLeases = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Current_Portof_LT_Debt_Capital_Leases'] = CurrentPortofLTDebtCapitalLeases

                OtherCurrentliabilitiesTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                # self.logger.info(OtherCurrentliabilitiesTotal)
                item['Other_Current_liabilities_Total'] = OtherCurrentliabilitiesTotal                

                TotalLiabilities = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]/td[%s]/text()"%(count+1)).extract()[2] 
                # self.logger.info(TotalLiabilities)
                
                item['Total_Liabilities'] = TotalLiabilities

                TotalLongTermDebt = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Long_Term_Debt'] = TotalLongTermDebt

                LongTermDebt = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Long_Term_Debt'] = LongTermDebt

                CapitalLeaseObligations = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Capital_Lease_Obligations'] = CapitalLeaseObligations

                TotalDebt = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Debt'] = TotalDebt

                DeferredIncomeTax = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Deferred_Income_Tax'] = DeferredIncomeTax

                MinorityInterest = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                item['Minority_Interest'] = MinorityInterest

                OtherLiabilitiesTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]//table/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Liabilities_Total'] = OtherLiabilitiesTotal

                TotalEquity = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[9]/td[%s]/text()"%(count+1)).extract()[2] 
                # self.logger.info(TotalEquity)
                item['Total_Equity'] = TotalEquity

                RedeemablePreferredStockTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Redeemable_Preferred_Stock_Total'] = RedeemablePreferredStockTotal

                PreferredStockNonRedeemableNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Preferred_Stock_Non_Redeemable_Net'] = PreferredStockNonRedeemableNet

                CommonStockTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Common_Stock_Total'] = CommonStockTotal

                AdditionalPaidInCapital = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Additional_Paid_In_Capital'] = AdditionalPaidInCapital
                
                RetainedEarningsAccumulatedDeficit = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Retained_Earnings_Accumulated_Deficit'] = RetainedEarningsAccumulatedDeficit
                
                TreasuryStockCommon = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                item['Treasury_Stock_Common'] = TreasuryStockCommon
                
                ESOPDebtGuarantee = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first()
                item['ESOP_Debt_Guarantee'] = ESOPDebtGuarantee
                
                UnrealizedGainLoss = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[8]/td[%s]/text()"%(count+1)).extract_first()
                item['Unrealized_Gain_Loss'] = UnrealizedGainLoss
                
                OtherEquityTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[10]//table/tbody/tr[9]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Equity_Total'] = OtherEquityTotal

                TotalLiabilitiesShareholdersEquity = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[11]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Liabilities_Shareholders_Equity'] = TotalLiabilitiesShareholdersEquity

                TotalCommonSharesOutstanding = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[12]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Common_Shares_Outstanding'] = TotalCommonSharesOutstanding

                TotalPreferredSharesOutstanding = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[13]/td[%s]/text()"%(count+1)).extract_first() 
                item['Total_Preferred_Shares_Outstanding'] = TotalPreferredSharesOutstanding

                count = count + 1
                yield item

        if count>1:                
            log_txt = base_url + ", BalanceSheet, " + self.select_param      
            self.makeLog(log_txt)

                # return

    def getCashFlow(self, response):

        self.logger.info("============= getCashFlow ===============")

        item = GetcashflowItem()

        base_url = response.meta['url']
        symbid = response.meta['symbid']
        freq = response.meta['freq']

        item['Symb'] = symbid
        item['Freq'] = freq

        count = 1
        datePaths = response.xpath('//tr[@class="alignBottom"]/th')
        for datePath in datePaths:

            dateYear = ''.join(datePath.xpath('span[@class="bold"]/text()').extract()).strip()
            dateDay = ''.join(datePath.xpath('div[@class="noBold arial_11"]/text()').extract()).strip()

            if dateYear and dateDay:

                self.logger.info("--------------------------------")
                date = dateDay + "/" + dateYear
                item['Date'] = date

                PeriodLength = response.xpath("//tr[@class='secondRow']/th[%s]/span/text()"%(count+1)).extract_first() 
                item['Period_Length'] = PeriodLength

                NetIncomStartingLine = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first() 
                item['Net_Incom_Starting_Line'] = NetIncomStartingLine

                CashFromOperatingActivities = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first() 
                item['Cash_From_Operating_Activities'] = CashFromOperatingActivities

                DepreciationDepletion = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Depreciation_Depletion'] = DepreciationDepletion

                Amortization = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Amortization'] = Amortization

                DeferredTaxes = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Deferred_Taxes'] = DeferredTaxes

                NonCashItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Non_Cash_Items'] = NonCashItems

                CashReceipts = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[5]/td[%s]/text()"%(count+1)).extract_first()
                item['Cash_Receipts'] = CashReceipts

                CashPayments = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[6]/td[%s]/text()"%(count+1)).extract_first()
                item['Cash_Payments'] = CashPayments

                CashTaxesPaid = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[7]/td[%s]/text()"%(count+1)).extract_first()
                item['Cash_Taxes_Paid'] = CashTaxesPaid

                CashInterestPaid = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[8]/td[%s]/text()"%(count+1)).extract_first()
                item['Cash_Interest_Paid'] = CashInterestPaid

                ChangesinWorkingCapital = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[3]//table/tbody/tr[9]/td[%s]/text()"%(count+1)).extract_first()
                item['Changesin_Working_Capital'] = ChangesinWorkingCapital

                CashFromInvestingActivities = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[4]/td[%s]/text()"%(count+1)).extract()[1] 
                item['Cash_From_Investing_Activities'] = CashFromInvestingActivities

                CapitalExpenditures = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[5]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Capital_Expenditures'] = CapitalExpenditures

                OtherInvestingCashFlowItemsTotal = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[5]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Other_Investing_Cash_Flow_Items_Total'] = OtherInvestingCashFlowItemsTotal

                CashFromFinancingActivities = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[6]/td[%s]/text()"%(count+1)).extract()[1] 
                item['Cash_From_Financing_Activities'] = CashFromFinancingActivities

                FinancingCashFlowItems = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]//table/tbody/tr[1]/td[%s]/text()"%(count+1)).extract_first()
                item['Financing_Cash_Flow_Items'] = FinancingCashFlowItems

                TotalCashDividendsPaid = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]//table/tbody/tr[2]/td[%s]/text()"%(count+1)).extract_first()
                item['Total_Cash_Dividends_Paid'] = TotalCashDividendsPaid

                IssuanceRetirementofStockNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]//table/tbody/tr[3]/td[%s]/text()"%(count+1)).extract_first()
                item['Issuance_Retirementof_Stock_Net'] = IssuanceRetirementofStockNet

                IssuanceRetirementofDebtNet = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[7]//table/tbody/tr[4]/td[%s]/text()"%(count+1)).extract_first()
                item['Issuance_Retirementof_DebtNet'] = IssuanceRetirementofDebtNet

                ForeignExchangeEffects = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[8]/td[%s]/text()"%(count+1)).extract()[1] 
                item['Foreign_Exchange_Effects'] = ForeignExchangeEffects

                NetChangeinCash = response.xpath("//table[@class='genTbl reportTbl']/tbody/tr[9]/td[%s]/text()"%(count+1)).extract()[1] 
                item['Net_Changein_Cash'] = NetChangeinCash   


                count = count + 1
                
                yield item

        if count>1:                
            log_txt = base_url + ", CashFlow, " + self.select_param        
            self.makeLog(log_txt)

                # return
    def makeLog(self, txt):

        standartdate = datetime.datetime.now()
        date = standartdate.strftime('%Y-%m-%d %H:%M:%S')
        fout = open("log.txt", "a")
        fout.write(str(date) + " -> " + txt + "\n")
        fout.close()

    def clearLog(self):
        fout = open("log.txt", "w")
        fout.close()
        # ipUrl = 'http://lumtest.com/myip.json'
        # proxy_ip_req = self.set_proxies(ipUrl, self.get_proxy_ip)
        # yield proxy_ip_req
        # return