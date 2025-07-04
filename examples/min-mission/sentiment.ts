import { poem } from "./poem";

export const sentiment = () => {
  const text = poem();
  // Mock sentiment analysis - in reality would use NLP
  const positiveWords = ['melted away', 'threads'];
  const score = positiveWords.some(word => text.includes(word)) ? 0.8 : 0.5;
  
  return { 
    text, 
    score,
    sentiment: score > 0.6 ? 'positive' : score < 0.4 ? 'negative' : 'neutral'
  };
};