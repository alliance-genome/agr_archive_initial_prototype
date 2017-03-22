Feature: navigate the search page

  Scenario Outline: Confirm results of search for <query>
      Given we open the search url querying for "<query>"
      When the search page returns
      Then "<id>" will be part of the first page of search results
      Examples: Genes
        | query  | id                 |
        | fgf8   | ZDB-GENE-990415-72 |
        | fgf8   | MGI:99604          |
        | mod-5  | WBGene00003387     |
        | POP8   | S000000114         |
        | TERF2  | 1322035            |
# These will require a better way to get at the id for GO terms, since they're not a link
#      Examples: GO Terms
#        | query               | id          |
#        | ubiquinone binding  | GO:0048039  |
#        | fin regeneration    | GO:0031101  |
#        | costamere           | GO:0043034  |
