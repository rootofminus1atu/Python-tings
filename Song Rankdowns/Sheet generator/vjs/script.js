/*
Spreadsheet generator for song rankdowns, by me. 
Originally written in python, translated into js.

To get it to work, paste all of this into a Google Apps Script project.
Make sure that you run the "createSpreadsheet" function.

This script creates a new google sheet each time you run it,
so remember to delete the failed attempts afterwards.

If you want to change the content of the cells, try to locate lines that look like:
`sheet.getRange(r, c).setValue("Nominated Songs:");`
*/

//=============================== Change these ==================================//

// Change these
const songs = [
  "Kanye West - Runaway",
  "kero kero bonito - flamingo",
  "Katamari Damacy - Lonely Rolling Star",
  "Beyonce - Formation",
  "Lizzo - Juice",
  "Lady Gaga - Bad Romance",
  "Hozier - Take Me To Church",
  "Kendrick Lamar - Alright",
  "Kendrick Lamar - King Kunta",
  "Kendrick Lamar - DNA",
  "Kendrick Lamar - Humble",
  "Arca - Bruja",
  "SOPHIE - Immaterial",
  "Porter Robinson - Shelter",
  "Yaeji - raingurl",
  "Charli XCX - Vroom Vroom",
  "Grimes - Oblivion",
  "Eminem - Rap God"
];
  
const users = [
  "joe",
  "jane",
  "sasha velour",
  "sasha fierce",
  "sasha obama",
  "sasha grey",
];

const nominationsNum = 5;  // how many nomination rows in each column

const fileName = "More tiers test AGAIN again";

//============================ You can change these ===============================//

// If you wanted to hae a grimace tier just add it to the list
// But then you also have to update colorGuide with your grimace colors
const generalColors = ["red", "orange", "yellow", "green"];
const top3Colors = ["bronze", "silver", "gold"];

const colorGuide = {
  red: {
    primary: '#EA9999',
    secondary: '#F4CCCC'
  },
  orange: {
    primary: '#F9CB9C',
    secondary: '#FCE5CD'
  },
  yellow: {
    primary: '#FFE599',
    secondary: '#FFF2CC'
  },
  green: {
    primary: '#B6D7A8',
    secondary: '#D9EAD3'
  },
  bronze: {
    primary: '#B45F06',
    secondary: '#E69138'
  },
  silver: {
    primary: '#B7B7B7',
    secondary: '#D9D9D9'
  },
  gold: {
    primary: '#BF9000',
    secondary: '#F1C232'
  },
  header_blue: {
    primary: '#4A86E8',
    secondary: '#4A86E8'
  },
  black: {
    primary: '#000000',
    secondary: '#000000'
  },
  gray: {
    primary: '#808080',
    secondary: '#808080'
  }  // don't forget commas when you're adding a new color here
};

const sizeGuide = {
  tiny: 15,
  smaller: 35,
  small: 60,
  medium: 200,
  big: 500,
  huge: 800,
};

const gapBetweenDecisionSpaces = 1;

//================== No touch (unless you know what you're doing) =====================//

function createSpreadsheet() {
  const spreadsheet = SpreadsheetApp.create(fileName);
  const sheet = spreadsheet.getActiveSheet();

  const colorRanges = getColorRangesWithSpecials(songs, generalColors, top3Colors);

  grayBorder(sheet, 1);
  songList(sheet, 1, 2, songs);
  console.log("Song list created");
  blackBorder(sheet, 3);
  scoreboard(sheet, 1, 4, colorRanges);
  console.log("Scoreboard created");
  blackBorder(sheet, 6);
  showtime(sheet, 1, 7, generalColors, top3Colors, colorRanges, users, nominationsNum);
  console.log("Nominations and decisions created");

  console.log("Done!")
}

function applyFormatting(sheet, r, c, color, bold = false, italic = false, underline = false) {
  const cell = sheet.getRange(r, c);

  if (color) {
    cell.setBackground(color);
  }
  
  if (bold) {
    cell.setFontWeight("bold");
  }
  
  if (underline) {
    cell.setFontLine('underline');
  }
  
  if (italic) {
    cell.setFontStyle("italic");
  }
}

function changeWidth(sheet, c, width) {
  sheet.setColumnWidth(c, width);
}

function songList(sheet, r, c, songs) {
  changeWidth(sheet, c, sizeGuide["big"]);

  sheet.getRange(r, c).setValue("List of Songs:");
  applyFormatting(sheet, r, c, colorGuide["header_blue"]["primary"], true);

  for (let i = 0; i < songs.length; i++) {
    sheet.getRange(r + 1 + i, c).setValue(songs[i]);
    applyFormatting(sheet, r + 1 + i, c, colorGuide["yellow"]["secondary"]);
  }
}

function scoreboard(sheet, r, c, colorRanges) {
  const first = c;
  const second = c + 1;
  changeWidth(sheet, first, sizeGuide["small"]);
  changeWidth(sheet, second, sizeGuide["big"]);

  sheet.getRange(r, first).setValue("Place:");
  applyFormatting(sheet, r, first, colorGuide["header_blue"]["primary"], true);
  sheet.getRange(r, second).setValue("Score:");
  applyFormatting(sheet, r, second, colorGuide["header_blue"]["primary"], true);

  for (let i = 0; i < songs.length; i++) {
    sheet.getRange(r + 1 + i, first).setValue(getOrdinalNumber(songs.length - i));
    applyFormatting(sheet, r + 1 + i, first, colorGuide[colorRanges[i]]["primary"], true);
  }

  for (let i = 0; i < songs.length; i++) {
    sheet.getRange(r + 1 + i, second).setValue("");
    applyFormatting(sheet, r + 1 + i, second, colorGuide[colorRanges[i]]["secondary"]);
  }
}

function decisionSpace(sheet, r, c, count, users, colorRanges) {
  const indx = colorRanges.length - count;

  const colorPrim = colorGuide[colorRanges[indx]]["primary"];
  const colorSec = colorGuide[colorRanges[indx]]["secondary"];

  sheet.getRange(r, c).setValue(`${getOrdinalNumber(count)} Place Vote: `);
  applyFormatting(sheet, r, c, colorPrim, true, false, true);
  sheet.getRange(r, c + 1).setValue("Explain Why You're Voting This Song: ");
  applyFormatting(sheet, r, c + 1, colorPrim, true, false, true);

  for (let i = 0; i < users.length; i++) {
    sheet.getRange(r + 1 + i, c).setValue(`${users[i]}'s Vote: `);
    applyFormatting(sheet, r + 1 + i, c, colorSec);
    sheet.getRange(r + 1 + i, c + 1).setValue("");
    applyFormatting(sheet, r + 1 + i, c + 1, colorSec);
  }

  sheet.getRange(r + 1 + users.length, c).setValue("Eliminated Song: ");
  applyFormatting(sheet, r + 1 + users.length, c, false, true);
}

function nominatedSongs(sheet, r, c, howManyNoms) {
  sheet.getRange(r, c).setValue("Nominated Songs:");
  applyFormatting(sheet, r, c, colorGuide["header_blue"]["primary"], true);
  sheet.getRange(r, c + 1).setValue("Nominated Song Link:");
  applyFormatting(sheet, r, c + 1, colorGuide["header_blue"]["primary"], true);

  for (let i = 0; i < howManyNoms; i++) {
    applyFormatting(sheet, r + 1 + i, c, colorGuide["yellow"]["secondary"]);
    applyFormatting(sheet, r + 1 + i, c + 1, colorGuide["yellow"]["secondary"]);
  }
}

function winner(sheet, r, c, colorRanges) {
  sheet.getRange(r, c).setValue("1st Place Winner: ");
  applyFormatting(sheet, r, c, colorGuide[colorRanges.slice(-1)]["primary"], true);
  applyFormatting(sheet, r, c + 1, colorGuide[colorRanges.slice(-1)]["primary"], true);
}

function blackBorder(sheet, c) {
  changeWidth(sheet, c, sizeGuide["tiny"]);

  const howLong = 200;
  for (let i = 1; i < howLong; i++) {
    applyFormatting(sheet, i, c, colorGuide["black"]["primary"]);
  }
}

function grayBorder(sheet, c) {
  changeWidth(sheet, c, sizeGuide["smaller"]);

  const howLong = 200;
  for (let i = 2; i < howLong; i++) {
    applyFormatting(sheet, i, c, colorGuide["gray"]["primary"]);
  }
  applyFormatting(sheet, 1, c, colorGuide["black"]["primary"]);
}

function showtime(
  sheet,
  r,
  c,
  generalColors,
  specialColors,
  colorRanges,
  users,
  howManyNoms
) {
  const nomDecGap = 2;
  const decStart = 1 + howManyNoms + 1 + nomDecGap;

  const nomIndexes = getNominationIndexes(r, c, generalColors);
  const decIndexes = getDecisionIndexes(
    decStart,
    c,
    generalColors,
    specialColors,
    colorRanges,
    users
  );
  const winnerIndex = decIndexes.pop();

  for (const [row, col] of nomIndexes) {
    changeWidth(sheet, col, sizeGuide["big"]);
    changeWidth(sheet, col + 1, sizeGuide["huge"]);
    nominatedSongs(sheet, row, col, howManyNoms);
  }

  let counter = colorRanges.length;
  for (const [row, col] of decIndexes) {
    decisionSpace(sheet, row, col, counter, users, colorRanges);
    counter--;
  }

  const [winnerRow, winnerCol] = winnerIndex;
  winner(sheet, winnerRow, winnerCol, colorRanges);

  for (const col of getBorderColumns(nomIndexes)) {
    blackBorder(sheet, col);
  }
}



// functions that don't depend on the context (can be reused in excel and anywhere else)

function getColorRanges(songs, colors) {
  var length = songs.length;

  var colorsCopy = [...colors].reverse();
  var colorList = [];
  for (var i = 0; i < length; i++) {
    colorList.push(colorsCopy[i % colorsCopy.length]);
  }

  var finalList = [];
  var jumpyIndex = 0;
  var tracker = 0;
  for (var i = 0; i < length; i++) {
    if (jumpyIndex >= length) {
      tracker += 1;
      jumpyIndex = tracker;
    }

    finalList.push(colorList[jumpyIndex]);

    jumpyIndex += colorsCopy.length;
  }

  finalList.reverse();
  return finalList;
}

function getColorRangesWithSpecials(songs, colors, specials) {
  var colorRanges = getColorRanges(songs.slice(0, -3), colors);
  return colorRanges.concat(specials);
}

function getDecisionIndexes(r, c, generalColors, top3Colors, colorRanges, users) {
  var gap = gapBetweenDecisionSpaces;
  var rowStep = 1 + users.length + 1 + gap;
  var colStep = 3;

  var indexes = [];

  for (var i = 0; i < generalColors.length; i++) {
    var targetCol = c + colStep * i;

    var howManyColors = colorRanges.filter(color => color === generalColors[i]).length;

    for (var j = 0; j < howManyColors; j++) {
      var targetRow = r + rowStep * j;
      indexes.push([targetRow, targetCol]);
    }
  }

  var targetRow = r + rowStep * howManyColors;
  for (var _ = 0; _ < top3Colors.length; _++) {
    indexes.push([targetRow, targetCol]);
    targetRow += rowStep;
  }

  return indexes;
}

function getNominationIndexes(r, c, generalColors) {
  var colStep = 3;

  var indexes = [];

  for (var i = c; i < c + colStep * generalColors.length; i += colStep) {
    indexes.push([r, i]);
  }

  return indexes;
}

function getBorderColumns(nomIndexes) {
  return nomIndexes.map(c => c[1] + 2);
}
  
function getOrdinalNumber(number) {
  const suffixes = {
    1: "st",
    2: "nd",
    3: "rd"
  };

  const teenSuffix = "th";

  const lastDigit = number % 10;
  const lastTwoDigits = number % 100;

  if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
    return number + teenSuffix;
  } else if (suffixes[lastDigit]) {
    return number + suffixes[lastDigit];
  } else {
    return number + "th";
  }
}
  
  
  