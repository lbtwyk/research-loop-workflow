# Correct an overgeneralized memory, not an additional delivery rule

On 2026-09-27 the user rejected unsolicited localhost URLs for the representation experiment video suite and explicitly requested finding and changing the source of this behavior, rather than adding a rule: “不是，你要找出为什么会给出网址，然后改掉这个，而不是加一条规则”. The three newly added workspace/video-delivery rules were removed.

The source is an overgeneralization of the pelican animation incident, thread 01a0d703-3735-7181-a75d-117f195f6a6e. In that incident, the user could not open a particular local HTML animation and an HTTP server was a successful workaround. This does not establish a general user preference or general inability to open local file/directory links.

Correct the existing memory source as follows, rather than adding a competing preference:

- Remove the general tip in memory_summary.md: “For local HTML, serve ... and verify HTTP 200; file:// is unreliable.” Remove the generalized “use localhost over file://” learning in its Local HTML/SVG topic.
- In MEMORY.md's “Local HTML/SVG visualization delivery” section, remove the imperative reuse_rule “reuse the serve-and-HTTP-check pattern” and the general instruction at line 203 to start a localhost HTTP service and present its URL instead. Retain only the scoped historical fact that this particular animation required a browser-serving workaround after a reported opening failure.
- Correct the corresponding overgeneralized “Failures and how to do differently” sentence in rollout_summaries/2026-09-25T05-21-47-O7JY-create_pelican_bicycle_svg_animation.md: do not extrapolate the one failed HTML opening into a future default for all generated HTML or local artifacts. Preserve the original incident and successful workaround as history.

The representation video renderer and catalog publisher write local artifacts; they do not require an HTTP server. The unsolicited URL was an assistant delivery decision caused by applying that memory outside its evidentiary scope. No new project prohibition or blanket rule about websites is requested.
