/**
 * Simulates Cô Julie's child-friendly evaluation for Hana's writing.
 * Used when no Gemini API Key is provided.
 */
function getSimulatedFeedback(content, targetVocab, hasImage = false) {
  let writingText = content;
  let transcription = undefined;

  if (hasImage) {
    transcription = `Yesterday, I decided to explore the dark woods behind my house. Suddenly, I found a beautiful cabin. It had an ancient wooden door. I pushed it and it creaked loudly. The room inside was very fragrant. I decided to investigate!`;
    writingText = transcription;
  }

  const wordCount = writingText.split(/\s+/).filter(w => w.length > 0).length;
  
  // Find which target vocab words were used
  const usedVocab = targetVocab.filter(word => 
    new RegExp(`\\b${word.toLowerCase()}\\b`, 'i').test(writingText)
  );

  let score = 5;
  if (wordCount > 10) score += 1;
  if (wordCount > 30) score += 1;
  if (wordCount > 60) score += 1;
  if (usedVocab.length >= 1) score += 1;
  if (usedVocab.length >= 3) score += 1;
  score = Math.min(score, 10);

  let grammarSpelling = "Tuyệt vời! Con viết các câu rất rõ ràng và dễ hiểu. Hầu hết các từ đều được viết đúng chính tả rồi đấy!";
  if (wordCount < 15) {
    grammarSpelling = "Bài viết hơi ngắn một chút. Con hãy viết thêm vài câu nữa và nhớ kiểm tra viết hoa chữ cái đầu câu và dấu chấm ở cuối câu nhé!";
  } else if (writingText.includes("i ") || /^[a-z]/.test(writingText)) {
    grammarSpelling = "Con viết rất tốt! Một lưu ý nhỏ là nhớ viết hoa chữ cái 'I' khi nói về bản thân và chữ cái đầu tiên của mỗi câu con nhé. Con sẽ làm tốt hơn ở lần tới!";
  }

  let vocabularyFeedback = `Bố mẹ thấy con đã sử dụng được các từ vựng rất hay. ${
    usedVocab.length > 0 
      ? `Chúc mừng con đã sử dụng được các từ khóa: **${usedVocab.join(", ")}** vào bài làm!` 
      : "Lần sau, con hãy thử kết hợp thêm các từ khóa gợi ý ở mục 'Target Vocabulary' để câu chuyện thêm sinh động nhé!"
  }`;

  let creativityFeedback = "Câu chuyện của con thật thú vị! Con có một trí tưởng tượng phong phú khi kể về chuyến phiêu lưu của mình. Hãy tiếp tục phát huy nhé!";
  if (writingText.toLowerCase().includes("dragon") || writingText.toLowerCase().includes("magic") || writingText.toLowerCase().includes("secret") || writingText.toLowerCase().includes("cabin")) {
    creativityFeedback = "Ồ! Câu chuyện có những chi tiết miêu tả bối cảnh cực kỳ lôi cuốn. Hana có tư duy kể chuyện và chọn góc nhìn rất tốt!";
  }

  let generalComment = `Cô Julie rất tự hào về Hana! ${
    hasImage 
      ? "Cô đã quét sạch sẽ ảnh chụp bài viết tay của con và tự động chuyển thành văn bản tiếng Anh rồi đó!" 
      : `Bài viết của con dài ${wordCount} từ và mang lại nhiều năng lượng tích cực.`
  } Hãy cố gắng luyện tập viết đều đặn mỗi ngày nhé! 🎉🌟`;

  return {
    score,
    grammarSpelling,
    vocabularyFeedback,
    creativityFeedback,
    generalComment,
    transcription
  };
}

/**
 * Calls Gemini API to evaluate Hana's writing.
 */
async function evaluateWriting(content, promptText, targetVocab, apiKey, base64Image) {
  const hasImage = !!base64Image && base64Image.trim() !== "";

  if (!apiKey || apiKey.trim() === "") {
    // Return simulated response after a short delay to mimic network request
    await new Promise(resolve => setTimeout(resolve, 2500));
    return getSimulatedFeedback(content, targetVocab, hasImage);
  }

  const systemInstruction = `
You are Teacher Julie, a friendly, encouraging, and experienced English teacher for Vietnamese children.
Your job is to evaluate the writing of a 9-year-old girl named Hana (Grade 4). She is good at speaking and listening but needs to improve writing.
Analyze her writing based on the prompt: "${promptText}" and target vocabulary: [${targetVocab.join(", ")}].

IF the user uploads an image of Hana's handwritten paper (which will be provided in the image part), you MUST read the handwriting, transcribe her written text exactly in English into the "transcription" field, and base your grading on that handwritten text.
If no image is provided, do NOT fill the "transcription" field.

You MUST return a JSON object with the following fields (and absolutely NO other text, do not put markdown wrappers other than JSON itself):
{
  "score": number (an integer from 1 to 10),
  "transcription": string (the exact transcription of her handwriting, ONLY if an image is provided. Otherwise, omit this field or return empty),
  "grammarSpelling": string (constructive, sweet feedback in Vietnamese, encouraging correct capitalization and punctuation. Use 2-3 sentences. Keep it positive!),
  "vocabularyFeedback": string (comment in Vietnamese about her word usage. Congratulate her if she used target vocabulary. Suggest 1-2 nice adjectives or verbs she could use. Use 2-3 sentences),
  "creativityFeedback": string (comment in Vietnamese celebrating her imagination and ideas. Use 2-3 sentences),
  "generalComment": string (a very warm, encouraging summary in Vietnamese. Add cute emojis! Praise her efforts. Use 2-3 sentences)
}

Guidelines for tone:
- Super encouraging, warm, and child-friendly.
- Write in clear, sweet Vietnamese.
- Point out errors gently (e.g., "Con nhớ viết hoa...", "Lần tới mình cùng...") instead of criticizing.
`;

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
    
    // Prepare contents array
    const parts = [];

    // Add image if available
    if (hasImage) {
      const match = base64Image.match(/^data:([^;]+);base64,(.+)$/);
      let mimeType = "image/jpeg";
      let data = base64Image;

      if (match) {
        mimeType = match[1];
        data = match[2];
      }

      parts.push({
        inlineData: {
          mimeType: mimeType,
          data: data
        }
      });
      parts.push({ text: `Analyze the writing on this image.` });
    }

    // Add text contents if available
    if (content && content.trim() !== "") {
      parts.push({ text: `Hana's written text on screen: ${content}` });
    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        contents: [
          {
            role: "user",
            parts: parts
          }
        ],
        systemInstruction: {
          parts: [{ text: systemInstruction }]
        },
        generationConfig: {
          responseMimeType: "application/json",
          temperature: 0.7
        }
      })
    });

    if (!response.ok) {
      throw new Error(`API returned status ${response.status}`);
    }

    const data = await response.json();
    const textResponse = data.candidates?.[0]?.content?.parts?.[0]?.text;
    
    if (!textResponse) {
      throw new Error("Empty response from Gemini API");
    }

    const result = JSON.parse(textResponse);
    
    return {
      score: typeof result.score === "number" ? result.score : 8,
      transcription: result.transcription || undefined,
      grammarSpelling: result.grammarSpelling || "Con viết câu rất tốt, lưu ý thêm về viết hoa đầu câu nhé!",
      vocabularyFeedback: result.vocabularyFeedback || "Từ vựng của con phong phú.",
      creativityFeedback: result.creativityFeedback || "Câu chuyện sáng tạo và thú vị.",
      generalComment: result.generalComment || "Cô Julie rất tự hào về con! 🥰🌟"
    };

  } catch (error) {
    console.error("Error calling Gemini API:", error);
    return getSimulatedFeedback(content, targetVocab, hasImage);
  }
}
