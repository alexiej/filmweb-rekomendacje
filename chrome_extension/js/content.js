// ==UserScript==
// @name        Filmweb.pl eksport ocen
// @namespace   kapela86
// @description Skrypt pozwala na eksport ocen oraz chcę/nie chcę zobaczyć/zagrać do plików xls. Działa na własnym profilu oraz znajomych.
// @include     http://www.filmweb.pl/user/*
// @include     https://www.filmweb.pl/user/*
// @include     http://filmweb.pl/user/*
// @include     https://filmweb.pl/user/*
// @version     1.7.3
// @grant       none
// @license     GPL-3.0-or-later
// @run-at      document-idle
// ==/UserScript==
"use strict";

/*
Changelog:
1.0		2015-04-14	pierwsze wydanie
1.1		2015-04-14	tytuły oryginalne są teraz klikalne i kierują do danego tytułu na stronie filmwebu
1.2		2015-04-21	dodano pobieranie komentarzy do ocen
1.3		2015-04-26	dodano pobieranie chcę/nie chcę zobaczyć/zagrać
1.4		2015-05-03	dodano pobieranie list znajomych
1.4.1	2015-05-04	różne drobne poprawki i optymalizacje kodu
1.4.2	2015-05-28	drobna poprawka dla osób mających spację w nicku
1.4.3	2016-11-27	poprawka dla osób które zainstalowały skrypt po 2016-10-04 i nie działał im przycisk zapisu do XLS
1.4.4	2017-07-09	naprawienie pobierania list "Chcę zobaczyć" (filmweb dodał kolumnę z datą dodania i to psuło wykonywanie skryptu)
1.5		2018-04-18	poprawienie skryptu aby mógł działać z nową wersją wyglądu profili i list ocen (na razie tylko pobieranie ocen zrobione)
1.6		2018-05-06	dodanie pobierania ocen programów tv i list "chcę zobaczyć/zagrać"
1.7		2018-05-27	dodanie pobierania list "nie interesuje mnie"
1.7.1	2018-05-29	poprawka dla nowego wyglądu strony profili
1.7.2	2018-07-22	poprawka drobnego błędu przy pobieraniu ocen
1.7.3	2019-04-14	poprawiłem błąd związany z nieładowaniem się skryptu i nieprawidłowym generowaniem odnośników do strony filmweb dla tytułów

To do:
- kompatybilność z greasemonkey 4
- eksport ocen aktorów i odcinków seriali


ExcellentExport.js v1.5
https://github.com/jmaister/excellentexport
https://raw.githubusercontent.com/jmaister/excellentexport/v1.5/excellentexport.min.js
*/
var n=String.fromCharCode,p;a:{try{document.createElement("$")}catch(q){p=q;break a}p=void 0} window.btoa||(window.btoa=function(b){for(var g,c,f,h,e,a,d=0,r=b.length,s=Math.max,l="";d<r;){g=b.charCodeAt(d++)||0;c=b.charCodeAt(d++)||0;a=b.charCodeAt(d++)||0;if(255<s(g,c,a))throw p;f=g>>2&63;g=(g&3)<<4|c>>4&15;h=(c&15)<<2|a>>6&3;e=a&63;c?a||(e=64):h=e=64;l+="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(f)+"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(g)+"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(h)+"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(e)}return l}); window.atob||(window.atob=function(b){b=b.replace(/=+$/,"");var g,c,f,h,e=0,a=b.length,d=[];if(1===a%4)throw p;for(;e<a;)g="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".indexOf(b.charAt(e++)),c="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".indexOf(b.charAt(e++)),f="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".indexOf(b.charAt(e++)),h="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".indexOf(b.charAt(e++)),g=(g&63)<< 2|c>>4&3,c=(c&15)<<4|f>>2&15,f=(f&3)<<6|h&63,d.push(n(g)),c&&d.push(n(c)),f&&d.push(n(f));return d.join("")});
var ExcellentExport=function(){function b(e,a){return e.replace(RegExp("{(\\w+)}","g"),function(d,e){return a[e]})}var g={excel:"data:application/vnd.ms-excel;base64,",csv:"data:application/csv;base64,"},c={excel:'<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\x3c!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--\x3e</head><body><table>{table}</table></body></html>'},f= ",",h="\r\n";return{excel:function(e,a,d){a=a.nodeType?a:document.getElementById(a);var f=g.excel;a=b(c.excel,{a:d||"Worksheet",table:a.innerHTML});a=window.btoa(window.unescape(encodeURIComponent(a)));e.href=f+a;return!0},csv:function(e,a,d,b){void 0!==d&&d&&(f=d);void 0!==b&&b&&(h=b);a=a.nodeType?a:document.getElementById(a);var c="",l,k;for(d=0;d<a.rows.length;d++){l=a.rows[d];for(b=0;b<l.cells.length;b++){k=l.cells[b];var c=c+(b?f:""),m=k.textContent.trim();k=m;var t=-1!==m.indexOf(f)||-1!==m.indexOf("\r")|| -1!==m.indexOf("\n");(m=-1!==m.indexOf('"'))&&(k=k.replace(/"/g,'""'));if(t||m)k='"'+k+'"';c+=k}c+=h}a=g.csv+window.btoa(window.unescape(encodeURIComponent(c)));e.href=a;return!0}}}();

var URL_SERVER = "http://filmy-rekomendacje.pl/render"
//var SERVER_STRON =
//console.log("This is ", window.extension_id)


// Arguments :
//  verb : 'GET'|'POST'
//  target : an optional opening target (a name, or "_blank"), defaults to "_self"

function openWindowWithPost(url, data) {
    var form = document.createElement("form");
    form.target = "_blank";
    form.method = "POST";
    form.action = url;
    form.style.display = "none";

    for (var key in data) {
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = key;
        input.value =  JSON.stringify(data[key]);
        form.appendChild(input);
//        console.log(key, JSON.stringify(data[key]))
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function tableToJson(table) {
    var data = [];
    // first row needs to be headers
    var headers = [];
    for (var i=0; i<table.rows[0].cells.length; i++) {
        headers[i] = table.rows[0].cells[i].innerHTML.toLowerCase().replace(/ /gi,'');
    }
    // go through cells
    for (var i=1; i<table.rows.length; i++) {
        var tableRow = table.rows[i];
        var rowData = {};
        for (var j=0; j<tableRow.cells.length; j++) {
//             text = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            rowData[ headers[j] ] = tableRow.cells[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ');
        }
        data.push(rowData);
    }
    return data;
}

function download_table_as_csv(table_id) {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(';'));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = 'export_' + table_id + '_' + new Date().toLocaleDateString() + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

try {


    var interval = setInterval(function() {
        if (typeof window.IRI == 'undefined') return;
        clearInterval(interval);

        // the rest of the code
        var NaszeID = window.IRI.deprecatedUser.id.toString();
        var IDWyswietlanegoUsera = document.querySelector("div.userPreview").getAttribute("data-id");
        var CzyZnajomy = Boolean(window.IRI.deprecatedUser.connections[IDWyswietlanegoUsera]);
        var NazwaProfilu = document.querySelector("div.userPreview").getAttribute("data-name");


        if ((CzyZnajomy || IDWyswietlanegoUsera === NaszeID) && window.location.pathname === "/user/" + NazwaProfilu.split(" ").join("+"))
        {
            var GlownyDiv = document.querySelector("div.pageContent section.flatContentWrapper");
            var MiejsceWstawienia = GlownyDiv.querySelector("section.sectionUserInfo");
            var KtoraStronaDoPobrania = 0;
            var IleStronZOcenami = 1;//wartość tutaj nie ma znaczenia bo później jest ładowana poprawna z kodu strony, ważne żeby tutaj była większa niż 0
            var KtoreElementy, NumerDiva, NumerPrzycisku, Tabela, RowSelector, CellSelector, IloscOcen, IloscPobranychOcen, filmNode, TempString, TempArray, TempNode, TempObject;
            var TablicaDivow = [
                {selektor: "EksportOcen_DivOceny", id: "eksportocen", tytul: "pobierz oceny:"},
//                {selektor: "EksportOcen_DivChcęZobaczyć", id: "eksportchce", tytul: "pobierz „chcę...”:"}
                //,
//                {selektor: "EksportOcen_DivNieChcęZobaczyć", id: "eksportnieinteresuje", tytul: "pobierz „nie interesuje ...”:"}
            ];
            var TablicaPrzyciskow = [
                [
                    {selektor: "EksportOcen_PrzyciskPobierzOcenyFilmow", tytul: "Statystyki filmweb-rekomendacje 🎬", id: "0,0", ktoreelementy: "id,tytulPL,tytulORG,rokprod,ulubione,ocena,komentarz,kraj,gatunek,data", parametr: "films?page=", plik: " - oceny - filmy.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzOcenySeriali", tytul: "seriale", id: "0,1", ktoreelementy: "id,tytulPL,tytulORG,rokprod,ulubione,ocena,komentarz,kraj,gatunek,data", parametr: "serials?page=", plik: " - oceny - seriale.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzOcenyGier", tytul: "gry", id: "0,2", ktoreelementy: "id,tytulPL,tytulORG,rokprod,ulubione,ocena,komentarz,gatunek,platformy,data", parametr: "games?page=", plik: " - oceny - gry.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzOcenyProgramowTV", tytul: "programy tv", id: "0,3", ktoreelementy: "id,tytulPL,tytulORG,rokprod,ulubione,ocena,komentarz,kraj,gatunek,data", parametr: "tvshows?page=", plik: " - oceny - programy tv.xls"},
//                    {selektor: "EksportOcen_PrzyciskZapiszOcenyDoXLS", tytul: "Zapisz do XLS", id: "zapisocen"}
                ]
//                [
//                    {selektor: "EksportOcen_PrzyciskPobierzChceZobaczycFilmy", tytul: "filmy", id: "1,0", ktoreelementy: "id,tytulPL,tytulORG,rokprod,jakbardzo,kraj,gatunek", parametr: "wantToSee?filmType=FILM&page=", plik: " - chcę zobaczyć - filmy.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzChceZobaczycSeriale", tytul: "seriale", id: "1,1", ktoreelementy: "id,tytulPL,tytulORG,rokprod,jakbardzo,kraj,gatunek", parametr: "wantToSee?filmType=SERIAL&page=", plik: " - chcę zobaczyć - seriale.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzChceZagrac", tytul: "gry", id: "1,2", ktoreelementy: "id,tytulPL,tytulORG,rokprod,jakbardzo,gatunek,platformy", parametr: "wantToPlay?page=", plik: " - chcę zagrać.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzChceZobaczycProgramyTV", tytul: "programy tv", id: "1,3", ktoreelementy: "id,tytulPL,tytulORG,rokprod,jakbardzo,kraj,gatunek", parametr: "wantToSee?filmType=TV_SHOW&page=", plik: " - chcę zobaczyć - programy tv.xls"},
//                    {selektor: "EksportOcen_PrzyciskZapiszChceZobaczycDoXLS", tytul: "Zapisz do XLS", id: "zapischce"}
//                ]
//                ,
//                [
//                    {selektor: "EksportOcen_PrzyciskPobierzNieInteresujeFilmy", tytul: "filmy", id: "2,0", ktoreelementy: "id,tytulPL,tytulORG,rokprod,kraj,gatunek", parametr: "dontWantToSee?filmType=FILM&page=", plik: " - nie interesuje - filmy.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzNieInteresujeSeriale", tytul: "seriale", id: "2,1", ktoreelementy: "id,tytulPL,tytulORG,rokprod,kraj,gatunek", parametr: "dontWantToSee?filmType=SERIAL&page=", plik: " - nie interesuje - seriale.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzNieInteresujeGry", tytul: "gry", id: "2,2", ktoreelementy: "id,tytulPL,tytulORG,rokprod,gatunek,platformy", parametr: "dontWantToSee?filmType=VIDEOGAME&page=", plik: " - nie interesuje - gry.xls"},
//                    {selektor: "EksportOcen_PrzyciskPobierzNieInteresujeProgramyTV", tytul: "programy tv", id: "2,3", ktoreelementy: "id,tytulPL,tytulORG,rokprod,kraj,gatunek", parametr: "dontWantToSee?filmType=TV_SHOW&page=", plik: " - nie interesuje - programy tv.xls"},
//                    {selektor: "EksportOcen_PrzyciskZapiszNieInteresujeDoXLS", tytul: "Zapisz do XLS", id: "zapisnieinteresuje"}
//                ]
            ];

            var ListaKolumn = {
                id: {
                    NaglowekTabeli: "ID",
                    CzyDodac: false
                },
                tytulPL: {
                    NaglowekTabeli: "Tytuł polski",
                    CzyDodac: false
                },
                tytulORG: {
                    NaglowekTabeli: "Tytuł oryginalny",
                    CzyDodac: false
                },
                rokprod: {
                    NaglowekTabeli: "Rok produkcji",
                    CzyDodac: false
                },
                jakbardzo: {
                    NaglowekTabeli: "Jak bardzo chcę",
                    CzyDodac: false
                },
                ulubione: {
                    NaglowekTabeli: "Ulubione",
                    CzyDodac: false
                },
                ocena: {
                    NaglowekTabeli: "Ocena",
                    CzyDodac: false
                },
                komentarz: {
                    NaglowekTabeli: "Komentarz",
                    CzyDodac: false
                },
                kraj: {
                    NaglowekTabeli: "Kraj produkcji",
                    CzyDodac: false
                },
                gatunek: {
                    NaglowekTabeli: "Gatunek",
                    CzyDodac: false
                },
                platformy: {
                    NaglowekTabeli: "Platformy",
                    CzyDodac: false
                },
                data: {
                    NaglowekTabeli: "Data",
                    CzyDodac: false
                }
            }

            for (var i = 0; i < TablicaDivow.length; i++)
            {
                window[TablicaDivow[i].selektor] = GlownyDiv.querySelector("div#" + TablicaDivow[i].id);
                if (window[TablicaDivow[i].selektor] !== null)
                {
                    GlownyDiv.removeChild(window[TablicaDivow[i].selektor]);
                }
                window[TablicaDivow[i].selektor] = document.createElement("div");
                window[TablicaDivow[i].selektor].id = TablicaDivow[i].id;
                window[TablicaDivow[i].selektor].style.marginBottom = "5px";
                window[TablicaDivow[i].selektor].style.marginTop = "25px";
                GlownyDiv.insertBefore(window[TablicaDivow[i].selektor], MiejsceWstawienia);
//                TempNode = document.createElement("span");
//                TempNode.textContent = TablicaDivow[i].tytul;
//                window[TablicaDivow[i].selektor].appendChild(TempNode);
                for (var j = 0; j < TablicaPrzyciskow[i].length; j++)
                {
                    window[TablicaPrzyciskow[i][j].selektor] = document.createElement("a");
                    window[TablicaPrzyciskow[i][j].selektor].style.cursor = "pointer";
                    window[TablicaPrzyciskow[i][j].selektor].style.margin = "20px 20px";
                     window[TablicaPrzyciskow[i][j].selektor].style.padding = "10px";

                      window[TablicaPrzyciskow[i][j].selektor].style["border-radius"] = "5px";
                    window[TablicaPrzyciskow[i][j].selektor].style.border = "1px solid silver";
                    window[TablicaPrzyciskow[i][j].selektor].style.background = "white";
                    window[TablicaDivow[i].selektor].appendChild(window[TablicaPrzyciskow[i][j].selektor]);
                }
            }
            Reset();
        }

        function Reset()
        {
            for (var i = 0; i < TablicaPrzyciskow.length; i++)
            {
                for (var j = 0; j < TablicaPrzyciskow[i].length; j++)
                {
                    window[TablicaPrzyciskow[i][j].selektor].textContent = TablicaPrzyciskow[i][j].tytul;
                    window[TablicaPrzyciskow[i][j].selektor].id = TablicaPrzyciskow[i][j].id;
                    if (j < 4)
                    {
                        window[TablicaPrzyciskow[i][j].selektor].addEventListener("click", PrzygotowanieDoPobierania, false);
                    }
                    else
                    {
                        window[TablicaPrzyciskow[i][j].selektor].addEventListener("click", Ostrzezenie, false);
                        window[TablicaPrzyciskow[i][j].selektor].style.color = "grey";
                    }
                    if (j === TablicaPrzyciskow[i].length-1)
                    {
                        window[TablicaPrzyciskow[i][j].selektor].removeAttribute("download");
                        window[TablicaPrzyciskow[i][j].selektor].removeAttribute("href");
                    }
                }
            }
            TempArray = Object.keys(ListaKolumn);
            for (var i = 0; i < TempArray.length; i++)
            {
                ListaKolumn[TempArray[i]].CzyDodac = false;
            }
            KtoraStronaDoPobrania = 0;
            IleStronZOcenami = 1;
            IloscPobranychOcen = 0;
//            EksportOcen_PrzyciskZapiszOcenyDoXLS.removeEventListener("click", ZapiszOcenyDoXLS, false);
//            EksportOcen_PrzyciskZapiszChceZobaczycDoXLS.removeEventListener("click", ZapiszChceZobaczycDoXLS, false);
//            EksportOcen_PrzyciskZapiszNieInteresujeDoXLS.removeEventListener("click", ZapiszNieInteresujeDoXLS, false);
        }

        function PrzygotowanieDoPobierania()
        {
            TempArray = this.id.split(",");
            NumerDiva = parseInt(TempArray[0]);
            NumerPrzycisku = parseInt(TempArray[1]);
            Reset();
            KtoreElementy = TablicaPrzyciskow[NumerDiva][NumerPrzycisku].ktoreelementy.split(",");
            for (var i = 0; i < KtoreElementy.length; i++)
            {
                ListaKolumn[KtoreElementy[i]].CzyDodac = true;
            }
            StworzTabelke();
            window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "pobieranie...";
            if (NumerDiva === 0)
            {
                PobierzOceny();
            }
            else if (NumerDiva === 1)
            {
                PobierzChce();
            }
            else if (NumerDiva === 2)
            {
                PobierzNieInteresuje();
            }
        }

        function PobierzOceny()
        {
            KtoraStronaDoPobrania++;
            console.log("Która strona do pobrania: " + KtoraStronaDoPobrania, "z " + IleStronZOcenami);
            if (KtoraStronaDoPobrania <= IleStronZOcenami)
            {
                var Request = new XMLHttpRequest();
                Request.onerror = function(){window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "błąd pobierania";};
                Request.onload = PrzetworzOceny;
                Request.open("GET", "//www.filmweb.pl/user/" + NazwaProfilu.split(" ").join("+") + "/" + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].parametr + KtoraStronaDoPobrania, true);
                Request.send();
            }
            else
            {
//                EksportOcen_PrzyciskZapiszOcenyDoXLS.removeEventListener("click", Ostrzezenie, false);
//                EksportOcen_PrzyciskZapiszOcenyDoXLS.addEventListener("click", ZapiszOcenyDoXLS, false);
//                EksportOcen_PrzyciskZapiszOcenyDoXLS.setAttribute("download", NazwaProfilu + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].plik);
//                EksportOcen_PrzyciskZapiszOcenyDoXLS.style.color = "";
//                chrome.tabs.create({url: 'rekomendacje.html'})
//                chrome.runtime.sendMessage({
//                 "Somethign": "showPageAction"
//                })
//                ZapiszOcenyDoXLS()
//                console.log(TablicaPrzyciskow[NumerDiva][NumerPrzycisku])

                window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].removeEventListener("click", PrzygotowanieDoPobierania, false);
                window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].addEventListener("click", PokazWyniki, false);

                window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "Pokaż statystyki (" + IloscPobranychOcen + " ocen) 🎬";
                PokazWyniki()
                KtoraStronaDoPobrania--;
            }
        }

        function PokazWyniki() {
                var table = document.querySelector("table#userscript");
                var dane = tableToJson(table)
                console.log(dane)

                openWindowWithPost(URL_SERVER, {'dane': dane})


//                download_table_as_csv("userscript")

//                window.io.open('POST', URL_SERVER, {'data': '2'}, '_blank');

//                var w = window.open(URL_SERVER, '_blank')
//
//                w.document.open()
//                w.document.write('dsafdasfds')
//                w.document.close()
//
//                for (var i = 0, row; row = table.rows[i]; i++) {
//                        console.log(row)
//
//                   //iterate through rows
//                   //rows would be accessed using the "row" variable assigned in the for loop
////                   for (var j = 0, col; col = row.cells[j]; j++) {
////
////                     //iterate through columns
////                     //columns would be accessed using the "col" variable assigned in the for loop
////                   }
//                }
//                console.log(chrome)
//chrome.runtime.sendMessage({
// 'message': "This is message s"
//})
//                window.open("https://www.google.pl") //"rekomendacje.html",'_blank');
//                window.open(url);
//            console.log('wyniki')
        }

        function PobierzChce()
        {
            KtoraStronaDoPobrania++;
            console.log("Która strona do pobrania: " + KtoraStronaDoPobrania, "z " + IleStronZOcenami);
            if (KtoraStronaDoPobrania <= IleStronZOcenami)
            {
                var Request = new XMLHttpRequest();
                Request.onerror = function(){window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "błąd pobierania";};
                Request.onload = PrzetworzChce;
                Request.open("GET", "//www.filmweb.pl/user/" + NazwaProfilu.split(" ").join("+") + "/" + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].parametr + KtoraStronaDoPobrania, true);
                Request.send();
            }
            else
            {
                EksportOcen_PrzyciskZapiszChceZobaczycDoXLS.removeEventListener("click", Ostrzezenie, false);
                EksportOcen_PrzyciskZapiszChceZobaczycDoXLS.addEventListener("click", ZapiszChceZobaczycDoXLS, false);
                EksportOcen_PrzyciskZapiszChceZobaczycDoXLS.setAttribute("download", NazwaProfilu + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].plik);
                EksportOcen_PrzyciskZapiszChceZobaczycDoXLS.style.color = "";
                KtoraStronaDoPobrania--;
            }
        }

        function PobierzNieInteresuje()
        {
            KtoraStronaDoPobrania++;
            console.log("Która strona do pobrania: " + KtoraStronaDoPobrania, "z " + IleStronZOcenami);
            if (KtoraStronaDoPobrania <= IleStronZOcenami)
            {
                var Request = new XMLHttpRequest();
                Request.onerror = function(){window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "błąd pobierania";};
                Request.onload = PrzetworzNieInteresuje;
                Request.open("GET", "//www.filmweb.pl/user/" + NazwaProfilu.split(" ").join("+") + "/" + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].parametr + KtoraStronaDoPobrania, true);
                Request.send();
            }
            else
            {
                EksportOcen_PrzyciskZapiszNieInteresujeDoXLS.removeEventListener("click", Ostrzezenie, false);
                EksportOcen_PrzyciskZapiszNieInteresujeDoXLS.addEventListener("click", ZapiszNieInteresujeDoXLS, false);
                EksportOcen_PrzyciskZapiszNieInteresujeDoXLS.setAttribute("download", NazwaProfilu + TablicaPrzyciskow[NumerDiva][NumerPrzycisku].plik);
                EksportOcen_PrzyciskZapiszNieInteresujeDoXLS.style.color = "";
                KtoraStronaDoPobrania--;
            }
        }

        function PrzetworzOceny()
        {
            TempArray = [];
            TempObject = {};
            var TempNode2;
            var Response = document.implementation.createHTMLDocument("");
            Response.documentElement.innerHTML = this.responseText;
            if (KtoraStronaDoPobrania === 1)
            {
                IloscOcen = Response.querySelector("span.blockHeader__titleInfoCount").textContent;
                IleStronZOcenami = Response.querySelector("section[data-pages-count]").getAttribute("data-pages-count");
            }
            var SpanUserVotes = Response.querySelector("span.dataSource[data-source=userVotes]");
            var ListaFilmow = SpanUserVotes.children;
            for (var i = 0, ID = ""; i < ListaFilmow.length; i++, IloscPobranychOcen++)
            {
                TempObject = JSON.parse(ListaFilmow[i].textContent);
//                console.log(TempObject);
                RowSelector = Tabela.insertRow();

                //ID
                CellSelector = RowSelector.insertCell();
                ID = TempObject.eId;
                CellSelector.textContent = ID;

                filmNode = Response.querySelector("div.voteBoxes__box[data-id=\"" + ID + "\"]");

                //Tytuł polski
                CellSelector = RowSelector.insertCell();
                TempNode2 = filmNode.querySelector("h3.filmPreview__title");
                if (TempNode2 !== null)
                {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Tytuł oryginalny
                CellSelector = RowSelector.insertCell();
                TempNode2 = filmNode.querySelector("div.filmPreview__originalTitle");
                if (TempNode2 !== null) {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Rok produkcji
                CellSelector = RowSelector.insertCell();
                TempNode = filmNode.querySelector("span.filmPreview__year");
                if (TempNode !== null) {
                    CellSelector.textContent = TempNode.textContent;
                }

                //Ulubione
                CellSelector = RowSelector.insertCell();
                if (TempObject.hasOwnProperty("f"))
                {
                    CellSelector.textContent = "tak";
                }

                //Ocena
                CellSelector = RowSelector.insertCell();
                if (TempObject.hasOwnProperty("r"))
                {
                    TempObject.r === 0 ? CellSelector.textContent = "brak oceny" : CellSelector.textContent = TempObject.r;
                }

                //Komentarz
                CellSelector = RowSelector.insertCell();
                if (TempObject.hasOwnProperty("c"))
                {
                    CellSelector.textContent = TempObject.c;
                }

                //Kraj produkcji
                if (ListaKolumn.kraj.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = filmNode.querySelector(".filmPreview__info--countries > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }

                //Gatunek
                CellSelector = RowSelector.insertCell();
                TempNode = filmNode.querySelector(".filmPreview__info--genres > ul");
                if (TempNode !== null)
                {
                    for (var j = 0; j < TempNode.children.length; j++)
                    {
                        if (j > 0)
                        {
                            CellSelector.textContent += ", ";
                        }
                        CellSelector.textContent += TempNode.children[j].textContent;
                    }
                }

                //Platformy
                if (ListaKolumn.platformy.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = filmNode.querySelector(".filmPreview__info--platforms > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }

                //Data
                CellSelector = RowSelector.insertCell();
                if (TempObject.hasOwnProperty("d"))
                {
                    if (TempObject.d.hasOwnProperty("y"))
                    {
                        CellSelector.textContent = TempObject.d.y;
                        if (TempObject.d.hasOwnProperty("m"))
                        {
                            CellSelector.textContent += "-" + TempObject.d.m;
                            if (TempObject.d.hasOwnProperty("d"))
                            {
                                CellSelector.textContent += "-" + TempObject.d.d;
                            }
                        }
                    }
                }
            }
            window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "pobrano " + IloscPobranychOcen + "/" + IloscOcen + " ocen";
            PobierzOceny();
        }

        function PrzetworzChce()
        {
            TempArray = [];
            TempObject = {};
            var TempNode2;
            var Response = document.implementation.createHTMLDocument("");
            Response.documentElement.innerHTML = this.responseText;
            if (KtoraStronaDoPobrania === 1)
            {
                IloscOcen = Response.querySelector("span.blockHeader__titleInfoCount").textContent;
                IleStronZOcenami = Response.querySelector("section[data-pages-count]").getAttribute("data-pages-count");
                //IleStronZOcenami = 2;
            }
            var ListaFilmow = Response.querySelectorAll("div.userVotesPage__results > div.userVotesPage__result");
            for (var i = 0, ID = ""; i < ListaFilmow.length; i++, IloscPobranychOcen++)
            {
                RowSelector = Tabela.insertRow();

                //ID
                CellSelector = RowSelector.insertCell();
                ID = ListaFilmow[i].getAttribute("data-id");
                CellSelector.textContent = ID;

                //Tytuł polski
                CellSelector = RowSelector.insertCell();
                TempNode2 = ListaFilmow[i].querySelector("h3.filmPreview__title");
                if (TempNode2 !== null)
                {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Tytuł oryginalny
                CellSelector = RowSelector.insertCell();
                TempNode2 = ListaFilmow[i].querySelector("div.filmPreview__originalTitle");
                if (TempNode2 !== null) {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Rok produkcji
                CellSelector = RowSelector.insertCell();
                TempNode = ListaFilmow[i].querySelector("span.filmPreview__year");
                if (TempNode !== null) {
                    CellSelector.textContent = TempNode.textContent;
                }

                //Jak bardzo chce
                CellSelector = RowSelector.insertCell();
                TempNode = ListaFilmow[i].querySelector("div.wantToSeeRateBox__message");
                if (TempNode !== null) {
                    CellSelector.textContent = TempNode.textContent;
                }

                //Kraj produkcji
                if (ListaKolumn.kraj.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = ListaFilmow[i].querySelector(".filmPreview__info--countries > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }

                //Gatunek
                CellSelector = RowSelector.insertCell();
                TempNode = ListaFilmow[i].querySelector(".filmPreview__info--genres > ul");
                if (TempNode !== null)
                {
                    for (var j = 0; j < TempNode.children.length; j++)
                    {
                        if (j > 0)
                        {
                            CellSelector.textContent += ", ";
                        }
                        CellSelector.textContent += TempNode.children[j].textContent;
                    }
                }

                //Platformy
                if (ListaKolumn.platformy.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = ListaFilmow[i].querySelector(".filmPreview__info--platforms > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }
            }
            window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "pobrano " + IloscPobranychOcen + "/" + IloscOcen + " wpisów";
            PobierzChce();
        }

        function PrzetworzNieInteresuje()
        {
            TempArray = [];
            TempObject = {};
            var TempNode2;
            var Response = document.implementation.createHTMLDocument("");
            Response.documentElement.innerHTML = this.responseText;
            if (KtoraStronaDoPobrania === 1)
            {
                IloscOcen = Response.querySelector("span.blockHeader__titleInfoCount").textContent;
                IleStronZOcenami = Response.querySelector("section[data-pages-count]").getAttribute("data-pages-count");
                //IleStronZOcenami = 2;
            }
            var ListaFilmow = Response.querySelectorAll("div.userVotesPage__results > div.userVotesPage__result");
            for (var i = 0, ID = ""; i < ListaFilmow.length; i++, IloscPobranychOcen++)
            {
                RowSelector = Tabela.insertRow();

                //ID
                CellSelector = RowSelector.insertCell();
                ID = ListaFilmow[i].getAttribute("data-id");
                CellSelector.textContent = ID;

                //Tytuł polski
                CellSelector = RowSelector.insertCell();
                TempNode2 = ListaFilmow[i].querySelector("h3.filmPreview__title");
                if (TempNode2 !== null)
                {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Tytuł oryginalny
                CellSelector = RowSelector.insertCell();
                TempNode2 = ListaFilmow[i].querySelector("div.filmPreview__originalTitle");
                if (TempNode2 !== null) {
                    TempNode = document.createElement("a");
                    TempNode.href = "https://www.filmweb.pl/entityLink?entityName=film&id=" + ID;
                    TempNode.textContent = TempNode2.textContent;
                    CellSelector.appendChild(TempNode);
                }

                //Rok produkcji
                CellSelector = RowSelector.insertCell();
                TempNode = ListaFilmow[i].querySelector("span.filmPreview__year");
                if (TempNode !== null) {
                    CellSelector.textContent = TempNode.textContent;
                }

                //Kraj produkcji
                if (ListaKolumn.kraj.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = ListaFilmow[i].querySelector(".filmPreview__info--countries > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }

                //Gatunek
                CellSelector = RowSelector.insertCell();
                TempNode = ListaFilmow[i].querySelector(".filmPreview__info--genres > ul");
                if (TempNode !== null)
                {
                    for (var j = 0; j < TempNode.children.length; j++)
                    {
                        if (j > 0)
                        {
                            CellSelector.textContent += ", ";
                        }
                        CellSelector.textContent += TempNode.children[j].textContent;
                    }
                }

                //Platformy
                if (ListaKolumn.platformy.CzyDodac === true)
                {
                    CellSelector = RowSelector.insertCell();
                    TempNode = ListaFilmow[i].querySelector(".filmPreview__info--platforms > ul");
                    if (TempNode !== null)
                    {
                        for (var j = 0; j < TempNode.children.length; j++)
                        {
                            if (j > 0)
                            {
                                CellSelector.textContent += ", ";
                            }
                            CellSelector.textContent += TempNode.children[j].textContent;
                        }
                    }
                }
            }
            window[TablicaPrzyciskow[NumerDiva][NumerPrzycisku].selektor].textContent = "pobrano " + IloscPobranychOcen + "/" + IloscOcen + " wpisów";
            PobierzNieInteresuje();
        }

        function ZapiszOcenyDoXLS()
        {
            return ExcellentExport.csv(EksportOcen_PrzyciskZapiszOcenyDoXLS, "userscript", "Oceny");
        }

        function ZapiszChceZobaczycDoXLS()
        {
            return ExcellentExport.excel(EksportOcen_PrzyciskZapiszChceZobaczycDoXLS, "userscript", "Chcę zobaczyć");
        }

        function ZapiszNieInteresujeDoXLS()
        {
            return ExcellentExport.excel(EksportOcen_PrzyciskZapiszNieInteresujeDoXLS, "userscript", "Nie interesuje");
        }

        function StworzTabelke()
        {
            Tabela = document.querySelector("table#userscript");
            if (Tabela !== null)
            {
                document.body.removeChild(Tabela);
            }
            Tabela = document.createElement("table");
            Tabela.id = "userscript";
            Tabela.style.display = "none";
            document.body.appendChild(Tabela);
            RowSelector = Tabela.insertRow();

            KtoreElementy = TablicaPrzyciskow[NumerDiva][NumerPrzycisku].ktoreelementy.split(",");
            for (var i = 0; i < KtoreElementy.length; i++)
            {
                ListaKolumn[KtoreElementy[i]].CzyDodac = true;
                CellSelector = document.createElement("th");
                CellSelector.textContent = ListaKolumn[KtoreElementy[i]].NaglowekTabeli;
                RowSelector.appendChild(CellSelector);
            }
        }

        function Ostrzezenie()
        {
            alert("Najpierw pobierz którąś kategorię");
        }

    }, 500);

}

catch(error) {
    console.error(error);
}