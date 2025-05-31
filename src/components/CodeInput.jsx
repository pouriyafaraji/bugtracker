import React, { useState, useCallback } from "react";
import { FaCloudUploadAlt } from "react-icons/fa";
import "./CodeInput.css";

function CodeInput({ onSubmit }) {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState("");
  const [fileError, setFileError] = useState("");

  const validateFile = (file) => {
    const validExtensions = {
      ".py": "python",
      ".php": "php",
      ".c": "c",
      ".cpp": "cpp",
      ".js": "javascript",
    };

    const extension = "." + file.name.split(".").pop().toLowerCase();
    if (!validExtensions[extension]) {
      setFileError(
        "فرمت فایل نامعتبر است. لطفا فقط فایل‌های .py, .php, .c, .cpp, .js را آپلود کنید."
      );
      return false;
    }

    setLanguage(validExtensions[extension]);
    setFileError("");
    return true;
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      if (validateFile(file)) {
        setFileName(file.name);
        const reader = new FileReader();
        reader.onload = (event) => {
          setCode(event.target.result);
        };
        reader.onerror = () => {
          setFileError("خطا در خواندن فایل");
        };
        reader.readAsText(file);
      }
    }
  }, []);

  const handleFileUpload = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      if (validateFile(file)) {
        setFileName(file.name);
        const reader = new FileReader();
        reader.onload = (event) => {
          setCode(event.target.result);
        };
        reader.onerror = () => {
          setFileError("خطا در خواندن فایل");
        };
        reader.readAsText(file);
      }
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim()) {
      alert("لطفا کد مورد نظر خود را وارد کنید.");
      return;
    }

    setLoading(true);
    setShowResult(false);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, language }),
      });

      const data = await response.json();
      setResult(data.result);
      setShowResult(true);
      if (onSubmit) onSubmit({ code, language });
    } catch (error) {
      console.error("Error sending code:", error);
      setResult({ error: "خطا در اتصال به سرور" });
      setShowResult(true);
    } finally {
      setLoading(false);
    }
  };

  const renderIssues = (issues, language) => {
    if (!issues || issues.length === 0) {
      return (
        <div className="success-message">
          {language === "python"
            ? "هیچ خطایی یافت نشد! کد شما از نظر pylint معتبر است."
            : language === "php"
            ? "هیچ خطایی یافت نشد! کد شما از نظر PHPStan معتبر است."
            : language === "javascript"
            ? "هیچ خطایی یافت نشد! کد شما از نظر JSHint معتبر است."
            : "هیچ خطایی یافت نشد! کد شما از نظر Cppcheck معتبر است."}
        </div>
      );
    }

    return issues.map((issue, index) => (
      <div key={index} className={`issue-item ${issue.type.toLowerCase()}`}>
        <div className="issue-header">
          <span className="issue-type">{issue.type}</span>
          <span className="issue-line">خط {issue.line}</span>
        </div>
        <div className="issue-message">{issue.message}</div>
        <div className="issue-symbol">کد خطا: {issue.symbol}</div>
      </div>
    ));
  };

  return (
    <div className="container">
      <p className="top-paragraph box-shadow">
        {language === "python"
          ? "کد پایتون خود را وارد کنید تا با استفاده از pylint تحلیل شود."
          : language === "php"
          ? "کد PHP خود را وارد کنید تا با استفاده از PHPStan تحلیل شود."
          : language === "javascript"
          ? "کد JavaScript خود را وارد کنید تا با استفاده از JSHint تحلیل شود."
          : "کد C خود را وارد کنید تا با استفاده از Cppcheck تحلیل شود."}
      </p>

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "10px" }}
      >
        <div>
          <label htmlFor="language" style={{ marginRight: "10px" }}>
            زبان برنامه‌نویسی:
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="p-2 border rounded bg-gray-50"
          >
            <option value="python">Python</option>
            <option value="php">PHP</option>
            <option value="c">C</option>
            <option value="cpp">C++</option>
            <option value="javascript">JavaScript</option>
          </select>
        </div>

        <div
          className={`code-input-wrapper box-shadow ${
            isDragging ? "dragging" : ""
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {!code && (
            <div className="upload-icon">
              <FaCloudUploadAlt />
              <p>بکشید و رها کنید.</p>
            </div>
          )}
          <textarea
            className="code-textarea"
            placeholder="کد خود را اینجا وارد کنید..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={6}
          />
        </div>

        <div className="file-upload">
          <input
            type="file"
            id="fileInput"
            onChange={handleFileUpload}
            accept=".py,.php,.c,.cpp,.js"
            style={{ display: "none" }}
          />
          <input
            type="text"
            value={fileName}
            placeholder="نام فایل انتخاب شده"
            readOnly
            className="file-name-input"
          />
          <button
            type="button"
            onClick={() => document.getElementById("fileInput").click()}
            className="upload-button"
          >
            بارگذاری فایل
          </button>
        </div>
        {fileError && <div className="file-error">{fileError}</div>}

        <button
          type="submit"
          style={{
            padding: "10px 20px",
            backgroundColor: "#1a73e8",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
          disabled={loading}
        >
          {loading ? "درحال تحلیل..." : "تحلیل کد"}
        </button>
      </form>

      {showResult && result && (
        <div className="result-box box-shadow">
          {result.error ? (
            <div className="error-message">{result.error}</div>
          ) : (
            renderIssues(result.issues, language)
          )}
        </div>
      )}
    </div>
  );
}

export default CodeInput;
