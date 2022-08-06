

<template>
  <div>
    <div class="controls">
      <div>
        <label for="thickness">Thickness</label>
        <input type="range" min="1" max="100" v-model.number="thickness" id="thickness">
        <span>{{thickness}}</span>
      </div>
      <div>
        <label for="radius">Radius</label>
        <input type="range" min="1" max="400" v-model.number="radius" id="radius">
        <span>{{radius}}</span>
      </div>
      <div>
        <label for="color">Color</label>
        <input type="color" v-model="color" id="color">
      </div>
    </div>
    <svg width="800" height="800">



      <path v-for="part in parts" :key="part" :fill="color"
        :d="describeLogoPart(400, 400, radius, thickness, part * (360 / parts))" />

      <template v-if="showConstructionLines">
        <line x1="400" y1="400" x2="400" y2="0" style="stroke:rgb(0,0,0,0.5);stroke-width:1" />
        <line x1="200" :y1="400 - radius" x2="600" :y2="400 - radius" style="stroke:rgb(0,0,0,0.5);stroke-width:1" />

        <circle cx="400" cy="400" :r="radius" stroke="black" stroke-width="1" fill="none" />
        <circle cx="400" cy="400" :r="radius + 0.5 * thickness" stroke="black" stroke-width="1" fill="none" />
        <circle cx="400" cy="400" :r="radius - 0.5 * thickness" stroke="black" stroke-width="1" fill="none" />
      </template>



    </svg>
  </div>

</template>

<script >
export default {
  name: 'App',
  data(){
    return {
      radius: 200,
      thickness: 50,
      parts: 3,
      color: '#c00000',

    }
  },
  methods: {

    degToRad(angleInDegrees){
      return (angleInDegrees - 90) * Math.PI / 180.0
    },
    radToDeg(angleInRadians) {
      return angleInRadians * 180.0  / Math.PI 
    },

    polarToCartesian(centerX, centerY, radius, angleInDegrees) {
      const angleInRadians = this.degToRad(angleInDegrees)

      return {
        x: centerX + (radius * Math.cos(angleInRadians)),
        y: centerY + (radius * Math.sin(angleInRadians))
      };
    },

    quadraticFormula({a,b,c}){
      return {
        x1: (-b - Math.sqrt(Math.pow(b, 2) - (4 * a * c))) / (2 * a),
        x2: (-b + Math.sqrt(Math.pow(b, 2) - (4 * a * c))) / (2 * a),
      }
    },



    describeLogoPart(x, y, radius, thickness, angle){

      const startAngle = angle
      const endAngle = startAngle + 360 / this.parts

      const t = thickness
      const innerRadius = radius - (thickness /2)
      const outerRadius = radius + (thickness / 2)


      const { x1: startDX } = this.quadraticFormula({ a: 2, b: 2 * (t - innerRadius), c: Math.pow(t, 2) })
      const { x1: endDx } = this.quadraticFormula({ a: 2, b: -2 * (t + outerRadius), c: Math.pow(t, 2) })

      console.log({startDX, endDx})


      const alpha = this.radToDeg(Math.asin((t + startDX) / innerRadius))
      const gamma = this.radToDeg(Math.asin((t - endDx) / outerRadius))


      const innerStart = this.polarToCartesian(x, y, innerRadius, endAngle)
      const innerEnd = this.polarToCartesian(x, y, innerRadius, startAngle + alpha)

      const outerStart = this.polarToCartesian(x, y, outerRadius, endAngle - gamma)
      const outerEnd = this.polarToCartesian(x, y, outerRadius, startAngle )


      return [
        "M", innerStart.x, innerStart.y,
        "A", innerRadius, innerRadius, 0, 0, 0, innerEnd.x, innerEnd.y,
        // "L", innerEnd.x, innerEnd.y,
        "L", outerEnd.x, outerEnd.y,
        "A", outerRadius, outerRadius, 0, 0, 1, outerStart.x, outerStart.y,
        // "L", outerStart.x, outerStart.y,
        "L", innerStart.x, innerStart.y,
      ].join(" ");

    }


  }

}
</script>

<style>
svg {
  border: 1px solid #dddddd;
}
</style>
