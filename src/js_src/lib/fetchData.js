/*eslint-disable no-undef */
let oldRequest = {};

export default function fetchData(_url, options={}) {
  let _type = options.type || 'GET';
  return new Promise(function (resolve, reject) {
    // setTimeout(() => reject(new Error('request timeout')), timeout);
    if (typeof oldRequest.abort === 'function') oldRequest.abort();
    // *** DEPENDS ON GLOBAL $ because $ can abort ***
    oldRequest = $.ajax({
      url : _url,
      type : _type,
      dataType:'json',
      success: data => {
        resolve(data);
      },
      error: (request, e) => {
        if (e === 'abort') {
          return;
        }
        reject(e);
      }
    });
  });
}
