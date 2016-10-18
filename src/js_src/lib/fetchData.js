/*eslint-disable no-undef */

const TIMEOUT = 5000;

let xhrRequest = { readyState: 0 };
export default function fetchData(_url, options={}) {
  let _type = options.type || 'GET';
  return new Promise(function (resolve, reject) {
    // abort old request if not complete
    if (xhrRequest.readyState === 1) {
      xhrRequest.abort();
    }
    // *** DEPENDS ON GLOBAL $ because $ can abort ***
    xhrRequest = $.ajax({
      url : _url,
      type : _type,
      dataType:'json',
      timeout: TIMEOUT,
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
