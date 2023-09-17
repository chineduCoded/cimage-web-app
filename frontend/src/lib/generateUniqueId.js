export const generateUniqueId = (length = 64) => {
    // Define characters to choose from for the session ID
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  
    // Generate a random component using the crypto API
    let randomPart = '';
    const crypto = window.crypto || window.msCrypto; // Check for browser support
    if (crypto) {
      const randomValues = new Uint8Array(length);
      crypto.getRandomValues(randomValues);
      randomPart = Array.from(randomValues, (value) => characters[value % characters.length]).join('');
    } else {
      // Fallback to less secure Math.random()
      for (let i = 0; i < length; i++) {
        randomPart += characters.charAt(Math.floor(Math.random() * characters.length));
      }
    }
  
    return randomPart;
  }
  