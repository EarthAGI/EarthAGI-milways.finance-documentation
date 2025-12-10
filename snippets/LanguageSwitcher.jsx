import React from 'react';

const LanguageSwitcher = ({ currentPath }) => {
  // 從當前路徑判斷語言
  const getCurrentLang = () => {
    if (currentPath.startsWith('/zh-CN/')) return 'zh-CN';
    if (currentPath.startsWith('/zh/')) return 'zh';
    if (currentPath.startsWith('/ja/')) return 'ja';
    if (currentPath.startsWith('/ko/')) return 'ko';
    return 'en';
  };

  // 生成其他語言的路徑
  const getOtherLangPath = (targetLang) => {
    const currentLang = getCurrentLang();
    const pathWithoutLang = currentPath.replace(/^\/(en|zh|zh-CN|ja|ko)\//, '/');
    return `/${targetLang}${pathWithoutLang}`;
  };

  const currentLang = getCurrentLang();

  const languages = [
    { code: 'en', label: '🇺🇸 English' },
    { code: 'zh', label: '🇹🇼 繁體中文' },
    { code: 'zh-CN', label: '🇨🇳 简体中文' },
    { code: 'ja', label: '🇯🇵 日本語' },
    { code: 'ko', label: '🇰🇷 한국어' }
  ];

  return (
    <div style={{
      padding: '1rem',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      marginBottom: '2rem',
      border: '1px solid #e9ecef'
    }}>
      <div style={{ 
        fontSize: '0.875rem', 
        fontWeight: '600', 
        marginBottom: '0.5rem',
        color: '#495057'
      }}>
        🌐 選擇語言 / Select Language
      </div>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        {languages.map(({ code, label }) => (
          <a
            key={code}
            href={getOtherLangPath(code)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: currentLang === code ? '600' : '400',
              backgroundColor: currentLang === code ? '#0ABAB5' : '#ffffff',
              color: currentLang === code ? '#ffffff' : '#495057',
              border: `1px solid ${currentLang === code ? '#0ABAB5' : '#dee2e6'}`,
              transition: 'all 0.2s',
              cursor: 'pointer'
            }}
            onMouseOver={(e) => {
              if (currentLang !== code) {
                e.target.style.backgroundColor = '#e9ecef';
              }
            }}
            onMouseOut={(e) => {
              if (currentLang !== code) {
                e.target.style.backgroundColor = '#ffffff';
              }
            }}
          >
            {label}
          </a>
        ))}
      </div>
    </div>
  );
};

export default LanguageSwitcher;
