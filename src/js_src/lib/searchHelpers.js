import _ from 'underscore';

const NON_HIGHLIGHTED_FIELDS = ['sourceHref'];
const JOIN_HIGHLIGHT_BY = '...';

// takes the fields in responseObj.highlights and replaces the shallow values in responseObj
// also return highlight values as strings like '<em>val</em>...<em>val2</em>' instead of array
export function injectHighlightIntoResponse(responseObj) {
  let high = responseObj.highlights || {};
  let highKeys = Object.keys(high);
  let simpleHighObj = {};
  highKeys.forEach( key => {
    let highArr = high[key];
    let highStr = highArr.reduce( (prev, current, i) => {
      let suffix = (i === highArr.length - 1) ? '' : JOIN_HIGHLIGHT_BY;
      return prev + current + suffix;
    }, '');
    simpleHighObj[key] = highStr;
    // don't highlight some fields
    if (NON_HIGHLIGHTED_FIELDS.indexOf(key) < 0) {
      responseObj[key] = highStr;
    }
  });
  responseObj.highlights = simpleHighObj;
  return responseObj;
}

export function makeFieldDisplayName(unformattedName) {
  return unformattedName.replace('_', ' ');
}

export function getQueryParamWithValueChanged(key, val, locationObj) {
  let qp = locationObj ? _.clone(locationObj.query) : {};
  qp[key] = val;
  if (key === 'go_names') {
    let newVals = locationObj.query.go_names ? [locationObj.query.go_names]: [];
    let isInside = (newVals.indexOf(val) >= 0);
    if (isInside) {
      newVals = _.without(newVals, val);
    } else {
      newVals.push(val);
    }
    qp[key] = newVals;
  }
  return qp;
}
