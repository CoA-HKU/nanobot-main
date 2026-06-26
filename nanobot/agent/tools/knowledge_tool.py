*** Begin Patch
*** Update File: nanobot/agent/tools/knowledge_tool.py
@@
     def _load_index(self) -> List[Dict[str, Any]]:
-        if self._index is not None:
-            return self._index
-        if not self.index_path.exists():
-            self._index = []
-            return self._index
-        try:
-            with open(self.index_path, "r", encoding="utf8") as f:
-                self._index = json.load(f)
-        except Exception:
-            self._index = []
-        return self._index
+        if self._index is not None:
+            return self._index
+
+        # Build a list of candidate index paths (configured path + sensible fallbacks)
+        tried_paths = [self.index_path]
+        if not self.index_path.exists():
+            tried_paths.append(Path.cwd() / "knowledge" / "index" / "index.json")
+            p = Path.cwd()
+            for _ in range(4):
+                p = p.parent
+                tried_paths.append(p / "knowledge" / "index" / "index.json")
+
+        for p in tried_paths:
+            if p.exists():
+                try:
+                    with open(p, "r", encoding="utf8") as f:
+                        self._index = json.load(f)
+                        # remember the successful path for future calls
+                        self.index_path = p
+                        break
+                except Exception as e:
+                    # surface JSON / encoding errors in CI logs for diagnosis
+                    import sys
+
+                    print(
+                        f"KnowledgeRetrievalTool: error loading index from {p!s}: {e!r}",
+                        file=sys.stderr,
+                    )
+                    # continue to next candidate path
+                    continue
+
+        if self._index is None:
+            # nothing worked — be explicit in logs so CI shows why search returned no results
+            import sys
+
+            print(
+                f"KnowledgeRetrievalTool: index not found; attempted paths: {[str(x) for x in tried_paths]}",
+                file=sys.stderr,
+            )
+            self._index = []
+        return self._index
@@
-        # If token-overlap on previews produced no results, fall back to
-        # searching the full fragment files referenced by the index. This
-        # ensures tests that search for words present in titles (but not in
-        # the text_preview) succeed in CI where regeneration of previews may
-        # not have been run.
-        if not results and index:
-            q = query.strip().lower()
-            fallback = []
-            for entry in index:
-                p = entry.get("path")
-                if not p:
-                    continue
-                full = KB_ROOT / Path(p)
-                try:
-                    text = full.read_text(encoding="utf8")
-                except Exception:
-                    # ignore missing/unreadable files and continue
-                    continue
-                if q in text.lower():
-                    fallback.append({
-                        "id": entry.get("id"),
-                        "path": entry.get("path"),
-                        "source": entry.get("source"),
-                        "score": 1,
-                        "text_preview": entry.get("text_preview"),
-                    })
-                    if len(fallback) >= top_k:
-                        break
-            if fallback:
-                return fallback
+        # If token-overlap on previews produced no results, fall back to
+        # searching the full fragment files referenced by the index (or the
+        # normalized fragments in the repo). This helps CI tests pass when
+        # index.json isn't available or previews don't contain the query.
+        if not results:
+            q = query.strip().lower()
+            fallback = []
+            # If the index is empty, still attempt to scan normalized/ to find
+            # matching fragments (helps CI where index.json may be missing).
+            entries_to_scan = index if index else []
+            if not entries_to_scan:
+                # scan the normalized directory under KB_ROOT
+                norm_dir = KB_ROOT / "normalized"
+                if norm_dir.exists():
+                    for p in norm_dir.rglob("*.md"):
+                        try:
+                            text = p.read_text(encoding="utf8")
+                        except Exception:
+                            continue
+                        if q in text.lower():
+                            fallback.append({
+                                "id": p.name,
+                                "path": str(p.relative_to(KB_ROOT)),
+                                "source": "fallback",
+                                "score": 1,
+                                "text_preview": None,
+                            })
+                            if len(fallback) >= top_k:
+                                break
+            else:
+                for entry in entries_to_scan:
+                    p = entry.get("path")
+                    if not p:
+                        continue
+                    full = KB_ROOT / Path(p)
+                    try:
+                        text = full.read_text(encoding="utf8")
+                    except Exception:
+                        continue
+                    if q in text.lower():
+                        fallback.append({
+                            "id": entry.get("id"),
+                            "path": entry.get("path"),
+                            "source": entry.get("source"),
+                            "score": 1,
+                            "text_preview": entry.get("text_preview"),
+                        })
+                        if len(fallback) >= top_k:
+                            break
+            if fallback:
+                return fallback
*** End Patch
