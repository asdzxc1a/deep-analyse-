# Prompt Template Step Extraction Design

## Goal

Make prompt dossier pages more reconstruction-ready by extracting actionable steps from prompt templates that store their real instructions inside fenced blocks.

## Problem

The current workflow extractor removes fenced blocks before semantic analysis. That was the right fix for diagrams and code examples, but it created a blind spot for prompt-template repos like `superpowers`, where many prompt files place the actual operating instructions inside fenced markdown blocks.

Current failure mode:
- prompt page exists
- triggers and roles may be present
- ordered steps are often empty or too shallow
- reconstruction guidance becomes thin because the extractor missed the main prompt body

## Design

### 1. Keep the current default for non-prompt artifacts

Skills, docs, and other markdown artifacts should continue to ignore fenced blocks by default so diagrams and code samples do not pollute semantic extraction.

### 2. Add prompt-aware fenced-block extraction

For `prompt` artifacts only:
- inspect fenced blocks
- include lines from blocks that look like natural-language prompt templates
- exclude lines that look like code or diagrams

Prompt-template lines we want:
- markdown headings like `## Your Job`
- numbered steps
- bullet lists of responsibilities
- imperative prose lines like `When done, report:`

Lines we still want to avoid:
- code syntax
- graph/diagram syntax
- shell or JSON noise

### 3. Strengthen step extraction for prompts

When prompt-template lines are available, treat them as valid workflow evidence for:
- ordered steps
- constraints
- approval or escalation guidance
- role inference

This should make prompt dossier pages materially more useful without changing the rest of the workflow system.

## Non-Goals

This slice does not:
- perform full prompt parsing
- use an LLM to infer missing steps
- change non-prompt fenced-block behavior

## Success Criteria

After this slice:
- prompt templates with instructions inside fenced blocks produce real extracted steps
- existing fenced-block regression protection for skills/docs still holds
- `superpowers` prompt pages become more reconstruction-ready in smoke output
