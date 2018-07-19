
curl -XDELETE 'http://localhost:9200/bi/' >/dev/null 2>&1

curl -XPUT 'http://localhost:9200/bi/' -d '{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "synonym": {
            "tokenizer": "standard",
            "filter": [
              "synonym", 
              "stemmer"
            ]
          }
        },
        "filter" : {
          "synonym" : {
              "type" : "synonym",
              "synonyms_path" : "synonyms.txt",
              "ignore_case" : true
          },
          "stemmer" : {
              "type" : "stemmer",
              "name" : "possessive_english"
          }
        }
      }
    }
  },
  "mappings": {

    "bi" : {
      "properties" : {
          "ID" : {
           "type" : "string"
        },
        "BusinessName" : {
           "type" : "text"
        },
        "UBRN" : {
           "type" : "string"
        },
        "IndustryCode" : {
           "type" : "long"
        },
        "LegalStatus" : {
           "type" : "keyword"
        },
        "TradingStatus" : {
           "type" : "keyword"
        },
        "Turnover" : {
           "type" : "keyword"
        },
        "EmploymentBands" : {
           "type" : "keyword"
        },
        "PostCode" : {
           "type" : "string"
        },
        "VatRefs" : {
           "type" : "string"
        },
        "PayeRefs" : {
           "type" : "string"
        },
        "CompanyNo" : {
           "type" : "string"
        }
      }
    }
  }
}'
