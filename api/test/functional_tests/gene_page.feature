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
    | HGNC:7881         | NOTCH1   |

    Examples: Rat
    | id                | symbol   |
    | RGD:70891         | Fgf8     |
    | RGD:1306349       | Fmn1     |
    | RGD:620796        | Srm      |

    Examples: Mouse
    | id                | symbol   |
    | MGI:109337        | Brca2    |
    | MGI:108202        | Pcbp2    |
    | MGI:2676586       | Foxo6    |
    | MGI:88180         | Bmp4     |
    | MGI:109583        | Pten     |
    | MGI:96765         | Ldlr     |
    | MGI:1916172       | Dnaic1   |
    | MGI:96680         | Kras     |

    Examples: Fish
    | id                   | symbol  |
    | ZFIN:ZDB-GENE-990415-72   | fgf8a   |
    | ZFIN:ZDB-GENE-030131-3445 | dicer1  |
    | ZFIN:ZDB-GENE-980526-388  | bmp2a   |
    | ZFIN:ZDB-GENE-010525-1 | slc4a1a |

    Examples: Fly
    | id                | symbol   |
    | FB:FBgn0083973       | dunk     |
    | FB:FBgn0037960       | mthl5    |
    | FB:FBgn0027296       | temp     |
    | FB:FBgn0033885       | DJ-1alpha |

    Examples: Worm
    | id                | symbol    |
    | WB:WBGene00044305    | rad-8     |
    | WB:WBGene00169423    | 21ur-9605 |
    | WB:WBGene00000987    | dhs-24    |

    Examples: Yeast
    | id                | symbol   |
    | SGD:S000003256        | THG1     |
    | SGD:S000003513        | YOR1     |
    | SGD:S000000119        | MCM2     |
    | SGD:S000001015        | NPR3     |
