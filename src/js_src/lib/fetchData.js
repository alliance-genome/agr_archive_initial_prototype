/*eslint-disable no-undef */
export default function fetchData(_url, options={}) {
  let _type = options.type || 'GET';
  return new Promise(function (resolve, reject) {
    // *** DEPENDS ON GLOBAL $ because $ can abort ***
    $.ajax({
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
