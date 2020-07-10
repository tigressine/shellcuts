package shellcuts.core.structures

import shellcuts.core.actions.Action

case class Command(action: Action, arguments: List[String])
