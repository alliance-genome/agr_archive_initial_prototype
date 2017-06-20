export const SEARCH_API_ERROR_MESSAGE = 'There was a problem connecting to the server. Please refresh the page.  If you continue to see this message, please contact alliance-software@lists.stanford.edu';
export const LARGE_COL_CLASS = 'col-sm-8 col-md-8 col-xs-12';
export const SMALL_COL_CLASS = 'col-sm-4 col-md-4 col-xs-12';
export const WP_REST_API_BASE_URL = 'https://public-api.wordpress.com/wp/v2/sites/alliancegenome.wordpress.com/pages?slug=';

export const CATEGORIES = [
  {
    name: 'all',
    displayName: 'All'
  },
  {
    name: 'gene',
    displayName: 'Genes'
  },
  {
    name: 'go',
    displayName: 'Gene Ontology'
  }
];

export const WP_PAGES ={
  home: {
    title: 'Home - Alliance of Genome Resources',
    label: 'Home',
    slug: 'home',
    path: 'home'
  },
  about: {
    title: 'About Us - Alliance of Genome Resources',
    label: 'About Us',
    slug: 'about-us',
    path: 'about'
  },
  projects: {
    title: 'Projects, Work Product, Publications - Alliance of Genome Resources',
    label: 'Projects, Work Product, Publications',
    slug: 'projects-work-products-publications',
    path: 'projects'
  },
  contact: {
    title: 'Contact Us - Alliance of Genome Resources',
    label: 'Contact Us',
    slug: 'contact-us',
    path: 'contact'
  },
  faq:{
    title: 'FREQUENTLY ASKED QUESTIONS - Alliance of Genome Resources',
    label: 'Frequently Asked Questions',
    slug: 'frequently-asked-questions',
    path: 'faq'
  },
  funding: {
    title: 'FUNDING - Alliance of Genome Resources',
    label: 'Funding',
    slug: 'funding',
    path: 'funding'
  },
  organization: {
    title: 'Organization and Governance - Alliance of Genome Resources',
    label: 'Organization and Governance',
    slug: 'organization-and-governance',
    path: 'organization'
  },
  goups: {
    title: 'Projects, Work Product, Publications - Alliance of Genome Resources',
    label: 'AGR Working Groups',
    slug: 'projects-work-products-publications',
    path: 'projects'
  },
  features: {
    title: 'Genome Features - Alliance of Genome Resources',
    label: 'Genome Features',
    slug: 'genome-features',
    path: 'features'
  },
  supplement: {
    title: 'Administrative Supplement - Alliance of Genome Resources',
    label: 'Administrative Supplement',
    slug: 'administrative-supplement',
    path: 'supplement'
  },
  orthology: {
    title: 'Orthology - Alliance of Genome Resources',
    label: 'Orthology',
    slug: 'orthology',
    path: 'orthology'
  },
  phenotypes: {
    title: 'Phenotypes And Disease Models - Alliance of Genome Resources',
    label: 'Phenotypes And Disease Models',
    slug: 'phenotypes-and-disease-models',
    path: 'phenotypes'
  },
  publications:{
    title: 'Publications - Alliance of Genome Resources',
    label: 'Publications',
    slug: 'publications',
    path: 'publications'
  }
};
export const MENU = [
  'home',
  'about',
  'projects',
  'contact'
];
export const SUB_MENU= {
  about: [
    'faq',
    'funding',
    'organization'
  ],
  projects: [
    'goups',
    'publications'
  ]
};
export const NON_HIGHLIGHTED_FIELDS = ['sourceHref', 'href', 'category', 'homologs', 'paralogs', 'orthologs', 'homologs.symbol', 'homologs.panther_family'];
