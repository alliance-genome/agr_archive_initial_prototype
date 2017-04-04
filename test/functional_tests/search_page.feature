Feature: navigate the search page

  Scenario Outline: Confirm results of search for <query>

      Given we open the search url querying for "<query>"
      When the search page returns
      Then "<linktext>" will be on the first page of search results

      Examples: Genes
        | query                     | linktext           |
        | fgf8                      | Fgf8               |
        | fgf8                      | fgf8a              |
        | mod-5                     | mod-5              |
        | POP8                      | POP8               |
        | early onset breast cancer | BRCA2              |

      Examples: GO Terms
        | query               | linktext             |
        | serotonin           | serotonin secretion  |
        | serotonin           | serotonin uptake     |
        | regenerating fin    | fin regeneration     |
        | costamere           | costamere            |
