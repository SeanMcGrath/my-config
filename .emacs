(require 'package)
(add-to-list 'package-archives
  '("melpa" . "http://melpa.milkbox.net/packages/") t)
(package-initialize)

(setq backup-directory-alist `(("." . "~/.saves")))

(defun require-package (package &optional min-version no-refresh)
  "Ask elpa to install given PACKAGE."
  (if (package-installed-p package min-version)
      t
    (if (or (assoc package package-archive-contents) no-refresh)
        (package-install package)
      (progn
        (package-refresh-contents)
        (require-package package min-version t)))))

;; Auto-install missing packages:
(require-package 'yasnippet)
(require-package 'auto-complete)
(require-package 'ac-dabbrev)
(require-package 'magit)
(require-package 'smartparens)
(require-package 'markdown-mode)
(require-package 'markdown-mode+)
(require-package 'scala-mode2)
(require-package 'lorem-ipsum)
;(require-package 'go-mode)
;(require-package 'go-snippets)
;(require-package 'go-autocomplete)
;(require-package 'go-direx)
;(require-package 'go-eldoc)
;(require-package 'go-errcheck)
(require-package 'fiplr) ; fuzzy find file
(require-package 'yaml-mode)
(require-package 'sql-indent)

;; Color themes
(require-package 'color-theme)
(require-package 'cyberpunk-theme)
(require-package 'color-theme-sanityinc-tomorrow)
(require-package 'professional-theme)
(require-package 'spacegray-theme)

;;; basic configuration
; set auto-indent on return
(define-key global-map (kbd "RET") 'newline-and-indent)
; auto-pair mode
(electric-pair-mode t)
; show matching braces
(show-paren-mode t)

;;; to load a theme:
; M-x load-theme

;;; yasnippet
;;; should be loaded before auto complete so that they can work together
(require 'yasnippet)
(yas-global-mode 1)

;;; auto complete mod
;;; should be loaded after yasnippet so that they can work together
(require 'auto-complete)
(add-to-list 'ac-dictionary-directories "~/.emacs.d/dict")
(require 'auto-complete-config)
(ac-config-default)

;;; set the trigger key so that it can work together with yasnippet on tab key,
;;; if the word exists in yasnippet, pressing tab will cause yasnippet to
;;; activate, otherwise, auto-complete will
(ac-set-trigger-key "TAB")
(ac-set-trigger-key "<tab>")

;;; JavaScript Setup
(setq js-indent-level 2)

;;; Go Setup
;(add-hook 'before-save-hook 'gofmt-before-save)

;;; sql setup
(eval-after-load "sql"
  (load-library "sql-indent"))

;;; Line number setup
(global-linum-mode 1)
(setq linum-format "%4d \u2502 ")


(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes (quote ("bb08c73af94ee74453c90422485b29e5643b73b05e8de029a6909af6a3fb3f58" "53e29ea3d0251198924328fd943d6ead860e9f47af8d22f0b764d11168455a8e" "e35ef4f72931a774769da2b0c863e11d94e60a9ad97fb9734e8b28c7ee40f49b" "82d2cac368ccdec2fcc7573f24c3f79654b78bf133096f9b40c20d97ec1d8016" "f0a99f53cbf7b004ba0c1760aa14fd70f2eabafe4e62a2b3cf5cabae8203113b" default))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
