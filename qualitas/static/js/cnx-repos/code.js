function getLatestCNXTag(repo) {
    tags_url = 'https://api.github.com/repos/' + repo + '/tags';
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        response = xhr.responseText;
        resp = JSON.parse(response);
        latest_tag = resp[0].name;

        newlink = document.createElement('a');
        newlink.innerHTML = latest_tag;
        newlink.setAttribute('target', '_blank');
        newlink.setAttribute('title', 'Click to compare to master');
        newlink.setAttribute('href', 'https://github.com/' + repo
          + '/compare/' + latest_tag + '...master');
        document.getElementById(repo).appendChild(newlink);

        }
      }
    xhr.open('GET', tags_url);
    xhr.send(null);
    }

  function getPypiVersion(repo) {
    // https://pypi.org/pypi/nebuchadnezzar/json
    pypi_url = 'https://pypi.org/pypi/' + repo + '/json';
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
        response = xhr.responseText;
        resp = JSON.parse(response);
        pypi_version = resp.info.version;

        newlink = document.createElement('a');
        newlink.innerHTML = pypi_version;
        newlink.setAttribute('target', '_blank');
        newlink.setAttribute('title', 'Visit project on pypi');
        newlink.setAttribute('href', 'https://pypi.org/project/' + repo);
        document.getElementById('pypi/'+ repo).appendChild(newlink);

        }
      }
    xhr.open('GET', pypi_url);
    xhr.send(null);
    }

    // for user input to look up the latest github tag
    function lookupLatestCNXTag(repo) {
      repo = document.getElementById("repo-input").value;
      //alert(repo);
      tags_url = 'https://api.github.com/repos/Connexions/' + repo + '/tags';
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
          response = xhr.responseText;
          resp = JSON.parse(response);
          text = 'latest github tag for ' + repo + ': ' + resp[0].name;
          alert(text);
          }
        }
      xhr.open('GET', tags_url, true);
      xhr.send(null);
    }
