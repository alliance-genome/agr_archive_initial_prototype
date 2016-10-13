import _ from 'underscore';

const SINGLE_VAL_FIELDS = ['mode', 'page'];
const CLEARING_FIELDS = ['category'];

export function makeFieldDisplayName(unformattedName) {
  switch(unformattedName) {
  case 'go_branch':
    return 'GO Branch';
  default:
    return unformattedName.replace('_', ' ');
  }
}

export function getQueryParamWithValueChanged(key, val, queryParams, isClear=false) {
  let qp = _.clone(queryParams || {});
  let oldVal = _.clone(qp[key]);
  let isSingleValField = (SINGLE_VAL_FIELDS.indexOf(key) > -1);
  if (isSingleValField || oldVal === null || typeof oldVal === 'undefined') {
    qp[key] = val;
    return qp;
  }
  if (typeof oldVal !== 'object') {
    oldVal = [oldVal];
  }
  let newVal;
  if (oldVal.indexOf(val) > -1) {
    newVal = _.without(oldVal, val);
  } else {
    newVal = oldVal;
    newVal.push(val);
  }
  qp[key] = newVal;
  if (CLEARING_FIELDS.indexOf(key) > -1) {
    qp = { q: qp.q };
    qp[key] = newVal;
    if (isClear) {
      delete qp[key];
    }
    return qp;
  }
  return qp;
}
