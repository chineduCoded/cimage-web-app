// Function to count lines in the text
export const countLines = (code) => {
    return code.split('\n').length;
  };

  // Function to count the maximum number of characters in a line
  export const countMaxCharacters = (code) => {
    const lines = code.split('\n');
    const maxChars = Math.max(...lines.map((line) => line.trim().length)); // Use line.trim() to remove leading and trailing spaces
    return maxChars;
  };