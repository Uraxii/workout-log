# `POST /v1/databases`: the payload this repo must render

Reference doc. Every normative statement below carries a
`developers.notion.com` URL. Nothing here comes from model memory.

This file replaces the authority of
`.claude/skills/intake/references/db-create.md:28-40`, which is wrong in three
places (see [Where the repo is wrong](#where-the-repo-is-wrong)).

## Capture metadata

| Field | Value |
|---|---|
| Facts captured | 2026-09-02 |
| `Notion-Version` header | `2026-03-11` |
| Header source | <https://developers.notion.com/reference/versioning> and the `notionVersion` parameter in the OpenAPI block on <https://developers.notion.com/reference/create-database> |
| Endpoint | `POST https://api.notion.com/v1/databases` |
| Endpoint source | <https://developers.notion.com/reference/create-database> |

`Notion-Version` is `required: true` on this endpoint and its schema is an
enum with exactly one member, `'2026-03-11'`
(<https://developers.notion.com/reference/create-database>, OpenAPI
`components.parameters.notionVersion`). Versioning states: "The
Notion-Version header must be included in all REST API requests"
(<https://developers.notion.com/reference/versioning>).

### Which page is current, which is legacy

The docs site carries two generations of several pages. This matters: the
legacy pages give a relation shape that the current API rejects.

| Page | Status | Evidence |
|---|---|---|
| <https://developers.notion.com/reference/create-database> | **Current.** Use this. | Listed in <https://developers.notion.com/llms.txt> as "Create a database and its initial data source." Carries the full OpenAPI schema for `post /v1/databases`. |
| <https://developers.notion.com/reference/create-a-database> | **Legacy.** Do not use. | The page body says: "Deprecated as of version 2025-09-03 / This page describes the API for versions up to and including 2022-06-28." Its left nav places it under "Databases (deprecated)". It tells you to "Refer to the new APIs instead: Create a database, Create a data source". |
| <https://developers.notion.com/reference/property-object> | **Current.** "Data source properties". | Listed in `llms.txt` line 63. Documents `relation.data_source_id`, `status`, `place`, `unique_id`. |
| <https://developers.notion.com/reference/property-schema-object> | **Legacy.** Do not use for relations. | Not listed in `llms.txt` at all. Its "Relation configuration" table still names `database_id` as the relation target, which the 2025-09-03 upgrade removed from the write path. Cited below only for the full `number.format` enum, which the current page defers to it for. |
| <https://developers.notion.com/docs/upgrade-guide-2025-09-03> | **Redirects.** | `HTTP/2 308` to <https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>. Verified with `curl -sSI` on 2026-09-02. |

Both pages that document the create body are version-gated to `2026-03-11`:
that is the only value the endpoint's `Notion-Version` enum accepts.

## Verdicts on the disputed claims

### a. `database_id` -> `data_source_id`: CONFIRMED

The upgrade exists. Under "What's changing" it states: "Most API operations
that used `database_id` now require a `data_source_id`" and "Several database
endpoints have moved or been restructured to support the new data model"
(<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>).

`POST /v1/databases` does now nest initial properties under
`initial_data_source.properties`. The same page, under "After (2025-09-03)":
"`properties` for the initial data source you're creating now go under
`initial_data_source[properties]` to better separate data source specific
properties vs. ones that apply to the entire database. Other parameters apply
to the database and continue to be specified at the top-level when creating a
database (`icon`, `cover`, `title`)."

The OpenAPI schema on
<https://developers.notion.com/reference/create-database> agrees:
`initial_data_source` resolves to `initialDataSourceRequest`, whose only key
is `properties`, typed `additionalProperties: propertyConfigurationRequest`.

### b. "Exactly one `title` property": CONFIRMED, with a primary quote

<https://developers.notion.com/reference/property-object#title> carries a
warning block, quoted verbatim:

> **All data sources require exactly one `title` property.**
> The API throws errors if you create a data source without a `title`
> property, or attempt to add or remove a `title` property.

Corroborated by
<https://developers.notion.com/guides/data-apis/working-with-databases>:
"Every database has exactly one property with the `\"title\"` type."

The prior agent's UNVERIFIED flag is retired. The rule is enforceable.

### c. Relation on create: `data_source_id`, and the discriminator is required

`data_source_id`, never `database_id`. The upgrade guide, under "Create or
update database": "**For relation properties**: You can no longer provide a
`database_id`. Notion continues to include both the `database_id` and
`data_source_id` in the *response* for convenience, but the *request* object
must **only contain `data_source_id`**"
(<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>).

The discriminator is **required**. In the OpenAPI on
<https://developers.notion.com/reference/create-database>,
`relationPropertyConfigurationRequest.relation` is an `allOf` of an object
with `required: [data_source_id]` and a `oneOf` over two branches: the
"Single Property" branch has `required: [single_property]`, the "Dual
Property" branch has `required: [dual_property]`. An object carrying neither
key matches no branch of the `oneOf`, so it fails validation. Send one.

The `type` key itself (`"type": "single_property"`) is documented as a `const`
but does not appear in any branch's `required` list, so it is optional.

Legacy contradiction to ignore: the unlisted
<https://developers.notion.com/reference/property-schema-object> calls `type`
an "optional enum" and names `database_id` as the target. That page describes
`2022-06-28`.

### d. Formula `expression`: accepted, and `prop("Load")` is the syntax

`expression` is accepted via the API.
`formulaPropertyConfigurationRequest.formula` is an object with a single
string key, `expression`
(<https://developers.notion.com/reference/create-database>).

`prop("Name")` is the required form for referencing another property.
<https://developers.notion.com/reference/property-object#formula> gives the
example value `"prop(\"Price\") / 2"`, an example table containing
`prop("Price") * 1.1` and `if(prop("In stock"), "yes", "no")`, and this note:

> * `prop("Name")` matches a property by its current name, but the saved
>   formula references the property by ID, so renaming the property later
>   doesn't break the formula.
> * Expressions are validated when you save them. An expression that doesn't
>   parse or type check — for example, a `prop()` reference to a property that
>   doesn't exist — returns a [`validation_error`](/reference/errors).
> * When you read the schema back, formula expressions use the same
>   `prop("Name")` syntax you write. If an expression can't be rendered
>   faithfully in this syntax, the API returns it in the internal reference
>   syntax (`{{notion:block_property:...}}`) instead; both forms are valid in
>   expressions you write.

A bare identifier such as `Load` is not a property reference. The expression
is validated at save time, so a wrong expression fails the create call rather
than degrading silently.

### e. `Notion-Version`: `2026-03-11`

"The latest version is `2026-03-11`"
(<https://developers.notion.com/reference/versioning>, and the same string in
the `notionVersion` parameter description on
<https://developers.notion.com/reference/create-database>).

`2026-03-11` introduces three breaking changes: `after` becomes `position` on
Append block children, `archived` becomes `in_trash`, and the `transcription`
block type becomes `meeting_notes`
(<https://developers.notion.com/guides/get-started/upgrade-guide-2026-03-11>).
None of the three touches `POST /v1/databases`. The 2025-09-03 shape stands
unchanged in 2026-03-11.

### f. `status` and `formula` on create: both CAN be created

The prior agent's retracted assertion was right to retract.
`propertyConfigurationRequest` on
<https://developers.notion.com/reference/create-database> is a `oneOf` that
lists both `statusPropertyConfigurationRequest` and
`formulaPropertyConfigurationRequest` among its 27 branches.

`statusPropertyConfigRequest` has one optional key, `options`, described as
"The initial status options. If not provided, defaults are created." So
`{"Status": {"status": {}}}` is a valid create-time property and Notion
supplies the default option set.

This repo needs neither. `schema/notion-schema.json` uses no `status`
property; `Sessions.Status` is declared `select`. The repo does use one
`formula`.

### g. Parent: `page_id` or `workspace`

The OpenAPI `parent` schema on
<https://developers.notion.com/reference/create-database> is an `allOf` of
`{type: enum[page_id, workspace]}` and a `oneOf` of two branches:

- **Page Id**: `required: [type, page_id]`, `type` is `const: page_id`.
- **Workspace**: `required: [type, workspace]`, `type` is `const: workspace`,
  `workspace` is `const: true`.

`parent` is the only member of the request body's `required` list.

The same page's prose: "Creates a database as a subpage in the specified
parent page, or as a private page at the workspace level, with the specified
`properties` schema set on its `initial_data_source`. Currently, the `parent`
of a new database must be a Notion page (`page_id` type) or a
[wiki database](https://www.notion.com/help/wikis-and-verified-pages)."

The upgrade guide's post-2025-09-03 example shows both forms:
`"parent": {"type": "workspace", "workspace": true} | {"type": "page_id", "page_id": "..."}`
(<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>).

**What this repo's agent must supply**: `{"type": "page_id", "page_id": "<uuid>"}`.
`workspace` is valid at the REST layer but the hosted MCP tool's `parent`
object accepts only `page_id` (see [MCP](#can-the-mcp-tool-express-this)), and
the repo's own flow already targets a blank page the user shares.

## Request envelope

Headers (<https://developers.notion.com/reference/create-database>, OpenAPI
`security: bearerAuth` plus `components.parameters.notionVersion`):

```
POST https://api.notion.com/v1/databases
Authorization: Bearer <token>
Content-Type: application/json
Notion-Version: 2026-03-11
```

Body. Only `parent` is required; every other key is optional. Annotations name
the page that proves each part.

```json
{
  "parent": {
    "type": "page_id",
    "page_id": "b55c9c91-384d-452b-81db-d1ef79372b75"
  },

  "title": [
    { "type": "text", "text": { "content": "Sets" } }
  ],

  "description": [
    { "type": "text", "text": { "content": "One row per set." } }
  ],

  "is_inline": false,

  "icon": { "type": "emoji", "emoji": "🏋" },

  "initial_data_source": {
    "properties": {
      "Set index":  { "number":       {} },
      "Notes":      { "rich_text":    {} },
      "Timestamp":  { "date":         {} },
      "is_amrap":   { "checkbox":     {} },
      "Set type":   { "select":       { "options": [
                        { "name": "warmup" },
                        { "name": "working" },
                        { "name": "backoff" },
                        { "name": "dropset" }
                    ] } },
      "equipment":  { "multi_select": { "options": [] } },
      "Session":    { "relation": {
                        "data_source_id": "a42a62ed-9b51-4b98-9dea-ea6d091bc508",
                        "type": "single_property",
                        "single_property": {}
                    } },
      "e1RM":       { "formula": {
                        "expression": "prop(\"Load\") / (1.0278 - 0.0278 * prop(\"Reps\"))"
                    } },
      "Title":      { "title": {} }
    }
  }
}
```

Key-by-key proof:

| Key | Required | Proof |
|---|---|---|
| `parent` | **yes** — the sole member of the body's `required` list | <https://developers.notion.com/reference/create-database> |
| `parent.type` | yes within its branch, `const: "page_id"` | same |
| `parent.page_id` | yes within the Page Id branch, `idRequest` (string) | same |
| `title` | no. Array of `richTextItemRequest`, `maxItems: 100`. "The title of the database." | same |
| `description` | no. Array of `richTextItemRequest`, `maxItems: 100`. | same |
| `is_inline` | no. Boolean, "Defaults to false." | same |
| `icon` | no. `pageIconRequest`: one of `file_upload`, `emoji`, `external`, `custom_emoji`, `icon`. | same |
| `cover` | no. `pageCoverRequest`: one of `file_upload`, `external`. | same |
| `initial_data_source` | no, but omit it and you get a data source with no schema. `initialDataSourceRequest` has exactly one key. | same |
| `initial_data_source.properties` | no per schema. Object keyed by property display name, each value a `propertyConfigurationRequest`. "Property schema for the initial data source, if you'd like to create one." | same |
| `initial_data_source.properties.<name>.description` | no. `propertyConfigurationRequestCommon.description`, string, `minLength: 1`, `maxLength: 280`. | same |

Notion Version 2026-03-11 does **not** accept a `properties` key at the top
level. That form is the `2022-06-28` shape
(<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>,
"Before" code sample).

### Response, and getting the `data_source_id`

The `200` response is a `oneOf` of `partialDatabaseObjectResponse` and
`databaseObjectResponse`
(<https://developers.notion.com/reference/create-database>).

- `partialDatabaseObjectResponse` has `required: [object, id]` and
  `additionalProperties: false`. It gives you the database id and nothing
  else.
- `databaseObjectResponse` includes `data_sources` in its `required` list.

The database object's `data_sources` field is "List of child data sources,
each of which is a JSON object with an `id` and `name`", example
`[{"id": "c174b72c-d782-432f-8dc0-b647e1c96df6", "name": "Tasks data source"}]`
(<https://developers.notion.com/reference/database>).

So the renderer reads the new data source id from `data_sources[0].id`. If the
partial response comes back instead, fetch it with
<https://developers.notion.com/reference/retrieve-database>. A database id is
**not** a data source id; the upgrade guide's whole premise is that the two
were split (<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>).

This is what forces the create order in this repo: Sessions, Exercises and
Locations must exist and yield data source ids before Sets and Sessions can
name them in a relation.

## Property-type table

One row per type used by `schema/notion-schema.json`. Shapes are copied from
the OpenAPI `components.schemas` block on
<https://developers.notion.com/reference/create-database>; prose descriptions
come from <https://developers.notion.com/reference/property-object>.

| Type | Create-time JSON | Required sub-keys | Gotchas | URL |
|---|---|---|---|---|
| `title` | `{"title": {}}` | `title` (the outer key). Its value is `emptyObject`: `properties: {}`, `additionalProperties: false`. | Exactly one per data source, no more, no fewer. The property's own `id` is always the literal string `"title"`. The `title` **property** and the database `title` are different things and both are needed. | <https://developers.notion.com/reference/property-object#title> |
| `rich_text` | `{"rich_text": {}}` | `rich_text`, value is `emptyObject`. | Empty object, not `null`. `additionalProperties: false` means any key inside is rejected. | <https://developers.notion.com/reference/property-object#rich-text> |
| `number` | `{"number": {}}` or `{"number": {"format": "dollar"}}` | `number`. `format` is optional. | `format` is typed `numberFormat: {type: string, example: number}` in the create OpenAPI, with no enum. The value list lives on the legacy page: `number`, `number_with_commas`, `percent`, `dollar`, `canadian_dollar`, `euro`, `pound`, `yen`, `ruble`, `rupee`, `won`, `yuan`, `real`, `lira`, `rupiah`, `franc`, `hong_kong_dollar`, `new_zealand_dollar`, `krona`, `norwegian_krone`, `mexican_peso`, `rand`, `new_taiwan_dollar`, `danish_krone`, `zloty`, `baht`, `forint`, `koruna`, `shekel`, `chilean_peso`, `philippine_peso`, `dirham`, `colombian_peso`, `riyal`, `ringgit`, `leu`, `argentine_peso`, `uruguayan_peso`, `singapore_dollar`. No `default` key exists. | <https://developers.notion.com/reference/property-object#number>, enum at <https://developers.notion.com/reference/property-schema-object#number-configuration> |
| `select` | `{"select": {"options": [{"name": "warmup"}]}}` | `select`. `options` optional; each option requires `name`. | `options` is `maxItems: 100`. Option keys: `name` (required), `color` (`selectColor` enum: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`), `description` (string or null). No `default` key exists — a select cannot carry a default value at create time. | <https://developers.notion.com/reference/property-object#select> |
| `multi_select` | `{"multi_select": {"options": []}}` | `multi_select`. `options` optional. | Same option object and same `maxItems: 100` as `select`. Omitting `options` is legal; Notion adds options as rows use them. | <https://developers.notion.com/reference/property-object#multi-select> |
| `checkbox` | `{"checkbox": {}}` | `checkbox`, value is `emptyObject`. | No configuration at all. | <https://developers.notion.com/reference/property-object#checkbox> |
| `date` | `{"date": {}}` | `date`, value is `emptyObject`. | No configuration at create time. Time zone and range live on the page property value, not the schema. | <https://developers.notion.com/reference/property-object#date> |
| `relation` | `{"relation": {"data_source_id": "<uuid>", "type": "single_property", "single_property": {}}}` | `relation`, and inside it `data_source_id`, plus exactly one of `single_property` or `dual_property`. | `database_id` is rejected in the write path. `single_property` is `emptyObject`. `dual_property` takes optional `synced_property_id` and `synced_property_name`. `type` is a `const` but is not in any `required` list. The related database must be shared with the connection. | <https://developers.notion.com/reference/property-object#relation> and <https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03> |
| `formula` | `{"formula": {"expression": "prop(\"Load\") * 2"}}` | `formula`. `expression` is a string and is not in a `required` list, but a formula with no expression computes nothing. | Reference other properties as `prop("Name")`. Expressions are validated on save; a `prop()` naming a property that does not exist returns `validation_error` (HTTP 400). No `null_when`, no conditional metadata — conditionals go inside the expression with `if(...)`. | <https://developers.notion.com/reference/property-object#formula> |

Types this repo does not use but the endpoint accepts, for completeness:
`status`, `rollup`, `unique_id`, `url`, `people`, `files`, `email`,
`phone_number`, `created_by`, `created_time`, `last_edited_by`,
`last_edited_time`, `button`, `location`, `verification`, `last_visited_time`,
`place` (<https://developers.notion.com/reference/create-database>,
`propertyConfigurationRequest`).

## Rules a validator can enforce

Each rule cites the page that proves it. A validator can run every one of
these against a rendered payload with no network call.

1. `Notion-Version` equals `2026-03-11`. The endpoint's header parameter is
   `required: true` with a single-member enum.
   <https://developers.notion.com/reference/create-database>
2. The body contains `parent`. It is the only entry in the body schema's
   `required` list.
   <https://developers.notion.com/reference/create-database>
3. `parent` is either `{"type": "page_id", "page_id": <string>}` or
   `{"type": "workspace", "workspace": true}`. Both keys of the chosen branch
   are required and `workspace` must be the literal `true`.
   <https://developers.notion.com/reference/create-database>
4. The body contains no top-level `properties` key. Data source properties
   live at `initial_data_source.properties` from `2025-09-03` onward.
   <https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>
5. `title`, when present, is an array of rich text item objects, not a string,
   with at most 100 elements.
   <https://developers.notion.com/reference/create-database>
6. `description`, when present, is an array of rich text item objects with at
   most 100 elements.
   <https://developers.notion.com/reference/create-database>
7. Every value in `initial_data_source.properties` carries exactly one type
   key drawn from `propertyConfigurationRequest`'s 27 branches. An unknown key
   matches no branch.
   <https://developers.notion.com/reference/create-database>
8. `initial_data_source.properties` contains exactly one property whose type
   key is `title`. Not zero, not two. "All data sources require exactly one
   `title` property."
   <https://developers.notion.com/reference/property-object#title>
9. Every `title`, `rich_text`, `date`, `checkbox` and `single_property`
   configuration object is `{}`. Each resolves to `emptyObject`, which sets
   `additionalProperties: false`.
   <https://developers.notion.com/reference/create-database>
10. Every `relation` configuration carries `data_source_id`. It is the sole
    entry in that branch's `required` list.
    <https://developers.notion.com/reference/create-database>
11. No `relation` configuration carries `database_id`. "the *request* object
    must **only contain `data_source_id`**".
    <https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>
12. Every `relation` configuration carries exactly one of `single_property` or
    `dual_property`. The `oneOf` has one branch per key and each branch
    requires its key, so an object with neither validates against no branch.
    <https://developers.notion.com/reference/create-database>
13. Every `select` and `multi_select` option object carries `name`. It is the
    only required option key.
    <https://developers.notion.com/reference/create-database>
14. `select.options` and `multi_select.options` hold at most 100 entries
    (`maxItems: 100`).
    <https://developers.notion.com/reference/create-database>
15. Every `color` on a select or multi-select option, when present, is one of
    `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`,
    `pink`, `red` (`selectColor`).
    <https://developers.notion.com/reference/create-database>
16. Every `formula.expression` references other properties as `prop("Name")`,
    never as a bare identifier, and every name inside `prop(...)` exists in
    the same data source's `properties`. A `prop()` reference to a property
    that does not exist returns `validation_error`.
    <https://developers.notion.com/reference/property-object#formula>
17. No property configuration carries a `default` key. No branch of
    `propertyConfigurationRequest` defines one; the only key shared by all
    branches is `description`.
    <https://developers.notion.com/reference/create-database>
18. Every property `description`, when present, is a string of 1 to 280
    characters (`propertyDescriptionRequest`).
    <https://developers.notion.com/reference/create-database>
19. The whole request body is at most 500KB, and any `text.content` inside a
    rich text object is at most 2000 characters.
    <https://developers.notion.com/reference/request-limits>
20. Calls are paced to an average of three requests per second per
    connection: "**Per connection** — an average of three requests per second,
    with some bursts beyond the average allowed."
    <https://developers.notion.com/reference/request-limits> Corroborates the
    figure already in `research/01-storage-options.md`.

### UNSOURCED — do not enforce

- **Maximum property count per data source.** Nothing on
  <https://developers.notion.com/reference/request-limits> or
  <https://developers.notion.com/reference/create-database> caps how many keys
  `initial_data_source.properties` may hold. `Sets` declares 30. No source
  found either way.
- **Maximum property-name length.** The size-limits table covers property
  *values*, not property *names*. No cap found.
- **Whether a data source with zero properties is legal.** `properties` is
  optional on `initialDataSourceRequest`, but rule 8 says a data source needs
  a `title` property. The two statements are not reconciled anywhere I found.
- **Whether `initial_data_source` accepts a `name`.** The 2026-03-11
  `initialDataSourceRequest` schema defines only `properties`, but the docs
  never say the data source name is unsettable. The created data source does
  come back with a `name`
  (<https://developers.notion.com/reference/database>).

## Where the repo is wrong

Paths are JSON Pointers into `schema/notion-schema.json` at head `c7a978f`.

### 1. `Sets` has no `title` property — breaks rule 8

`$.databases.Sets.properties` declares 30 properties. None has
`"type": "title"`. The full list: `Session`, `Exercise`, `Set index`,
`Set type`, `is_amrap`, `to_failure`, `RPE`, `RIR`, `Timestamp`,
`machine_setting`, `Side`, `reps_left`, `reps_right`, `Notes`, `Load`,
`Unit`, `load_kind`, `Reps`, `duration_s`, `distance`, `distance_unit`,
`level`, `interval_s`, `attempt`, `write_key`, `source_message_id`,
`Pain flag`, `confirm_line`, `stale`, `e1RM`.

"The API throws errors if you create a data source without a `title`
property" (<https://developers.notion.com/reference/property-object#title>).
The `Sets` create call fails as declared.

`Sessions`, `Exercises` and `Locations` each declare exactly one and pass:
`$.databases.Sessions.properties.Title`,
`$.databases.Exercises.properties.Name`,
`$.databases.Locations.properties.Name`.

### 2. The `e1RM` formula uses bare identifiers — breaks rule 16

```
$.databases.Sets.properties.e1RM.expression
  = "Load / (1.0278 - 0.0278 * Reps)"
```

`Load` and `Reps` are bare identifiers. The accepted form is
`prop("Load")` and `prop("Reps")`
(<https://developers.notion.com/reference/property-object#formula>). As
written, the expression fails validation on save and returns
`validation_error`.

The rendered form:

```json
"e1RM": {
  "formula": {
    "expression": "prop(\"Load\") / (1.0278 - 0.0278 * prop(\"Reps\"))"
  }
}
```

### 3. `e1RM.null_when` has no API home

```
$.databases.Sets.properties.e1RM.null_when
  = ["Reps > 10", "Set type != working"]
```

`formulaPropertyConfigurationRequest.formula` accepts one key, `expression`
(<https://developers.notion.com/reference/create-database>). There is no
`null_when`. The condition must be folded into the expression with `if(...)`,
whose accepted form is shown as `if(prop("In stock"), "yes", "no")`
(<https://developers.notion.com/reference/property-object#formula>). The
renderer must not emit `null_when` as a JSON key; rule 7 rejects it.

### 4. Five `default` values are not expressible — breaks rule 17

```
$.databases.Sets.properties["Set type"].default   = "working"
$.databases.Sets.properties.Side.default          = "both"
$.databases.Sets.properties["Pain flag"].default  = "none"
$.databases.Sets.properties.attempt.default       = 0
$.databases.Exercises.properties.implements.default = 1
$.databases.Sessions.properties.Status.default    = "open"
```

Neither `selectPropertyConfigurationRequest` nor
`numberPropertyConfigurationRequest` defines a `default`
(<https://developers.notion.com/reference/create-database>). These defaults
must be applied by the writer when it creates a row, not by the schema. The
renderer must drop them.

### 5. Relation targets are database *names*, and must resolve to data source ids

```
$.databases.Sets.properties.Session.database     = "Sessions"
$.databases.Sets.properties.Exercise.database    = "Exercises"
$.databases.Sessions.properties.Location.database = "Locations"
```

The schema names a sibling database. The payload needs a
`data_source_id`, which is a different id from the database id
(<https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03>).
The renderer must resolve name -> created database -> `data_sources[0].id`
(<https://developers.notion.com/reference/database>) and emit
`data_source_id`, plus a `single_property` or `dual_property` key per rule 12.

This is not a defect in the schema, which is deliberately API-agnostic. It is
a requirement on the renderer, and it is where
`.claude/skills/intake/references/db-create.md:36` gets it wrong.

### 6. Repo-only metadata keys the renderer must strip

These are declarations for the trainer skills, not API fields. A renderer that
passes them through breaks rule 7.

`frozen_at`, `rule`, `advisory_only`, `derived_from`, `range`, `written_by`,
`null_when`, `default`, `enum`, `database`. Found at, among others,
`$.databases.Sessions.properties.Date.frozen_at`,
`$.databases.Sessions.properties.week_index.derived_from`,
`$.databases.Sessions.properties.Readiness.range`,
`$.databases.Exercises.properties.fail_count.written_by`,
`$.databases.Sessions.properties.Cursor.advisory_only`.

`enum` is the input to `select.options` / `multi_select.options` and is
consumed, not passed through.

### What `.claude/skills/intake/references/db-create.md` gets wrong

Three rows and one skeleton, at lines 28-40 of that file:

| Line | Says | Correct |
|---|---|---|
| Type-mapping row for `relation` | "`database_id` = the already-created id of `properties.<name>.database`" | `data_source_id`, plus `single_property` or `dual_property`. Rules 10-12. |
| Type-mapping row for `formula` | "`expression` = the schema's `expression` string" | The schema's string must be rewritten to `prop("...")` form first. Rule 16. |
| Payload skeleton | `"title": "Sets"` and top-level `"properties"` | `"title"` is an array of rich text items; properties go under `initial_data_source.properties`. Rules 4 and 5. |

Its `"parent": {"page_id": "..."}` omits `"type": "page_id"`, which is in the
Page Id branch's `required` list
(<https://developers.notion.com/reference/create-database>). Its statement
that Notion Free is "rate-limited to roughly 3 requests per second" matches
the documented per-connection average
(<https://developers.notion.com/reference/request-limits>), though the limit
is per connection, not per plan.

## Can the MCP tool express this?

**No, not directly.** The hosted `notion-create-database` tool does not take
the REST body. It takes SQL DDL.

Notion's own MCP docs describe the tool only in prose: "`notion-create-database`
/ Creates a new Notion database, initial data source, and initial view with
the specified properties"
(<https://developers.notion.com/guides/mcp/mcp-supported-tools>). Notion MCP
is "a remote MCP server hosted by Notion" that "uses the Notion API"
(<https://developers.notion.com/guides/mcp/overview>), so it wraps the same
endpoint, but the docs publish no JSON schema for the tool.

The tool schema itself, read from this session's own tool registry on
2026-09-02 without connecting to any workspace, gives the real surface. It
is **not** a developers.notion.com source, so nothing below is an enforceable
rule.

- Inputs: `schema` (a `CREATE TABLE` statement) or `database_type` (one of
  `tasks`, `projects`, `skills`), plus optional `parent`, `title`,
  `description`. Exactly one of `schema` and `database_type`.
- `parent` accepts only `{"page_id": ..., "type": "page_id"}`. No `workspace`
  branch. Omitting it creates "a private page at the workspace level".
- Type syntax covers everything this repo needs:
  `TITLE`, `RICH_TEXT`, `DATE`, `CHECKBOX`, `NUMBER [FORMAT 'dollar']`,
  `SELECT('opt':color, ...)`, `MULTI_SELECT('opt':color, ...)`,
  `FORMULA('expression')`, `RELATION('data_source_id')` for a one-way relation
  and `RELATION('data_source_id', DUAL)` for two-way.
- `RELATION` takes a **data source id**, matching answer (c).
- "If no title property is provided, `\"Name\"` is auto-added." That would
  paper over violation 1 in `Sets` by inventing a `Name` column, rather than
  failing. The renderer should not rely on it.
- Column comments map to the property `description`: "Any column: COMMENT
  'description text'".
- No way to set a `default`, matching rule 17.

Consequence for this repo: a renderer targeting the hosted MCP tool emits SQL
DDL strings, not the JSON above. A renderer targeting REST directly emits the
JSON above. The two are not interchangeable, and
`.claude/skills/intake/references/db-create.md` currently describes a JSON
payload while naming the MCP tool. That mismatch needs settling before the
intake skill is built.

## Open questions

1. Does `notion-create-database`'s DDL `FORMULA('expression')` accept the same
   `prop("Name")` syntax, and how are the nested double quotes escaped inside
   a single-quoted DDL literal? Not documented on developers.notion.com.
2. Does the create response for this endpoint return the full
   `databaseObjectResponse` (with `data_sources`) or the partial one? The
   OpenAPI declares a `oneOf` and states no condition. A renderer must handle
   both and fall back to
   <https://developers.notion.com/reference/retrieve-database>.
3. Is there a cap on properties per data source? Unsourced above; `Sets` at 30
   is the repo's largest and is probably fine, but that is a guess.
4. Whether `Sets` should gain a real `title` property or take the auto-added
   `Name`. That is a schema decision for the repo, not an API fact.

## Sources

Every URL below was fetched on 2026-09-02. The markdown variants (`<url>.md`)
are the machine-readable form the docs site publishes and are byte-identical
in content to the rendered page; sha256 of the fetched bytes is recorded so a
later reader can tell whether the page moved under them.

| URL | sha256 of fetched bytes | Fetched as |
|---|---|---|
| <https://developers.notion.com/reference/create-database> | `57db268beee087fa7dce8f82ae8b6ddd10d87a0b7ecc4e87007da8a863b2b778` | `.md` |
| <https://developers.notion.com/reference/property-object> | `2cf2844bcb23a0909f0d2d4fb653e1de7179dc44a4d59e88dda2a34f035f4e36` | `.md` |
| <https://developers.notion.com/reference/versioning> | `9f23151d9d5c775bbc263a71cc68ddbcc2ada85813d9fb1f2796e2014a80a927` | `.md` |
| <https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03> | `d209b80354835c6507ea9bbbb15d370665029a8c81003bf8e8560e37f8bcdf82` | `.md` |
| <https://developers.notion.com/guides/get-started/upgrade-guide-2026-03-11> | `6c04a5981cc79a6fafbc1fd98fd145a3192776bbe887d69cae816c9b054056c6` | `.md` |
| <https://developers.notion.com/guides/data-apis/working-with-databases> | `1785a9a79cf033b6a75ffef9b21ba121506f418d4626a725e0f7c821cfb91db3` | `.md` |
| <https://developers.notion.com/guides/mcp/overview> | `96aaca98de2092fabc942772e956ad970871e0e5e9ae4ee99943bc2daa2f1030` | `.md` |
| <https://developers.notion.com/guides/mcp/mcp-supported-tools> | `5202631775b52f81c171f133dcc9001678615c7bafdb82582e36d2493953094e` | `.md` |
| <https://developers.notion.com/reference/request-limits> | `038eaa72228ed581ea77b1a60d3126f35f1be6677382e7c66dbe1e44f316e226` | `.md` |
| <https://developers.notion.com/reference/property-schema-object> (legacy) | `068cbb3014a6219095aa38ab4c957f26f3bcdfbf62a9be5ddba1d08c8fcaa06b` | `.md` |
| <https://developers.notion.com/reference/create-a-database> (legacy) | `6d5cfe90f7439811d2378497053cbcc8679d5837b43e3b050b71f96aa84bf326` | rendered HTML |

Also read, not quoted: <https://developers.notion.com/reference/database>,
<https://developers.notion.com/reference/create-a-data-source>,
<https://developers.notion.com/reference/data-source>,
<https://developers.notion.com/reference/update-data-source-properties>,
<https://developers.notion.com/llms.txt>.

Internal: `schema/notion-schema.json`,
`.claude/skills/intake/references/db-create.md`,
`research/01-storage-options.md` (rate limits, MCP OAuth).

Two conventions this file does not follow, because the task that produced it
was scoped to write this file and nothing else:

- No `research/sources/19-notion-database-create-api.tsv` companion, which
  every other file in `research/` has.
- No `llmwiki ingest` of the fetched pages into `.kb/sources/`. The sha256
  column above is the substitute provenance. Re-fetching each `.md` URL and
  comparing hashes reproduces exactly what this file was written from.
