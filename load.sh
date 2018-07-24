python3 csv_to_elastic.py \
    --elastic-address 'localhost:9200' \
    --csv-file sample.csv \
    --elastic-index 'bi' \
    --elastic-type business \
    --delimiter ',' \
    --json-struct '{
        "ID" : "%ID%",
        "BusinessName" : "%BusinessName%",
        "UBRN" : "%UBRN%",
        "IndustryCode" : "%IndustryCode%",
        "LegalStatus" : "%LegalStatus%",
        "TradingStatus" : "%TradingStatus%",
        "Turnover" : "%Turnover%",
        "EmploymentBands" : "%EmploymentBands%",
        "PostCode" : "%PostCode%",
        "VatRefs" : "%VatRefs%",
        "PayeRefs" : "%PayeRefs%",
        "CompanyNo" : "%CompanyNo%"
    }'
