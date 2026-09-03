# Packaging targets for the workout-trainer skills.
# See docs/build-plan.md s8 (layout) and s9 phase 7 (proofs).

SKILL_MANIFESTS := $(wildcard .claude/skills/*/SKILL.md)
SKILL_NAMES := $(notdir $(patsubst %/,%,$(dir $(SKILL_MANIFESTS))))
FIXTURES := $(wildcard fixtures/*/)

.PHONY: skills check

# Symlink every existing .claude/skills/<name> into .agents/skills/<name>
# (Codex discovery path) and zip them into dist/workout-trainer-skills.zip
# (claude.ai upload path). Safe to rerun: prunes stale links first.
skills:
	@mkdir -p .agents/skills
	@find .agents/skills -maxdepth 1 -xtype l -delete
	@for name in $(SKILL_NAMES); do \
		ln -sfn ../../.claude/skills/$$name .agents/skills/$$name; \
	done
	@echo "linked: $(SKILL_NAMES)"
	python3 tools/package/build_zip.py

# Every offline proof from docs/build-plan.md s9, plus the packaging
# validators from s9 phase 7. No Notion, no network.
check:
	python3 tools/catalog/build.py
	python3 library/check.py
	python3 tools/schema/check_e1rm.py
	python3 tools/intake/check_questions_docs.py
	python3 tools/mock-notion/notion_ddl.py
	@fixtures_failed=0; \
	for f in $(FIXTURES); do \
		if out=$$(python3 tools/mock-notion/replay.py "$$f" 2>&1); then \
			echo "PASS $$f"; \
		else \
			echo "FAIL $$f"; \
			echo "$$out"; \
			fixtures_failed=1; \
		fi; \
	done; \
	exit $$fixtures_failed
	python3 tools/package/check_frontmatter.py
	python3 tools/package/build_zip.py
	python3 tools/package/check_zip.py
	@if command -v claude >/dev/null 2>&1; then \
		claude plugin validate ./ || exit 1; \
	else \
		echo "claude binary not found: skipping claude plugin validate"; \
	fi
	@matches=$$(grep -rIlE -i \
		'nicole|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' \
		--exclude-dir=.git --exclude-dir=.nikki-agents \
		--exclude-dir=.handoffs --exclude-dir=.kb --exclude-dir=.beads \
		--exclude-dir=research --exclude-dir=docs \
		--exclude=Makefile . 2>/dev/null); \
	if [ -n "$$matches" ]; then \
		echo "user-data grep found matches:"; echo "$$matches"; exit 1; \
	fi
	@echo "check: all proofs green"
