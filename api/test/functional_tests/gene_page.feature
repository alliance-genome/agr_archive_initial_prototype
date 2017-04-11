Feature: navigating the gene page

  Scenario Outline: View <id> the gene page
      When we open the "<id>" gene page
      Then the gene page will return
      Then it will show the gene symbol as "<symbol>"

    Examples: Human
    | id                | symbol   |
    | HGNC:17889        | APEX2    |
    | HGNC:25818        | BRD9     |
    | HGNC:3686         | FGF8     |

    Examples: Rat
    | id                | symbol   |
    | RGD:70891         | Fgf8     |
    | RGD:1306349       | Fmn1     |
    | RGD:620796        | Srm      |

    Examples: Mouse
    | id                | symbol   |
    | MGI:MGI:109337        | Brca2    |
    | MGI:MGI:108202        | Pcbp2    |
    | MGI:MGI:2676586       | Foxo6    |

    Examples: Fish
    | id                   | symbol  |
    | ZFIN:ZDB-GENE-990415-72   | fgf8a   |
    | ZFIN:ZDB-GENE-030131-3445 | dicer1  |
    | ZFIN:ZDB-GENE-980526-388  | bmp2a   |

    Examples: Fly
    | id                | symbol   |
    | FBgn0083973       | dunk     |
    | FBgn0037960       | mthl5    |
    | FBgn0027296       | temp     |

    Examples: Worm
    | id                | symbol    |
    | WBGene00044305    | rad-8     |
    | WBGene00169423    | 21ur-9605 |
    | WBGene00000987    | dhs-24    |

    Examples: Yeast
    | id                | symbol   |
    | S000003256        | THG1     |
    | S000003513        | YOR1     |
    | S000000119        | MCM2     |
