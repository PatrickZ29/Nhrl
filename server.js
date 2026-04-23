import express from "express";
import GoogleGenerativeAI from "@google/generative-ai";

const app = express();
app.use(express.json());

// Pon tu API key aquí (mantenla privada)
const genAI = new GoogleGenerativeAI("AIzaSyDioEqSZ-2Ye_H47TUV-m1dLY6ZcwHDlS0");

app.post("/generar", async (req, res) => {
    try {
        const { prompt } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro-latest" });
        const result = await model.generateContent(prompt);
        const texto = await result.response.text();
        res.json({ texto });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(3000, () => console.log("Servidor escuchando en http://localhost:3000"));